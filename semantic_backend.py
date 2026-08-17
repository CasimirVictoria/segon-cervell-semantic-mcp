import os, sys, json, glob, hashlib, sqlite3, time, re
import numpy as np

# Base paths
BASE_DIR = os.path.expanduser("~/Documents/Segon_Cervell")
DB_DIR = os.path.expanduser("~/.local/share/segon_cervell")
DB_PATH = os.path.join(DB_DIR, "semantic_index.db")
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

os.makedirs(DB_DIR, exist_ok=True)

# -------------------------------------------------------------
# 1. DATABASE INITIALIZATION
# -------------------------------------------------------------
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path TEXT UNIQUE,
            file_type TEXT,
            mtime REAL,
            content_hash TEXT,
            title TEXT
        );
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS chunks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path TEXT,
            chunk_index INTEGER,
            start_line INTEGER,
            heading TEXT,
            content TEXT,
            embedding BLOB,
            FOREIGN KEY (file_path) REFERENCES files(file_path) ON DELETE CASCADE
        );
    """)
    conn.commit()
    return conn

# -------------------------------------------------------------
# 2. DOCUMENT PARSER & CHUNKER (Org-Mode, Markdown, Quarto)
# -------------------------------------------------------------
def parse_and_chunk_file(file_path):
    chunks = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as fp:
            lines = fp.readlines()
    except Exception:
        return "", []

    title = os.path.basename(file_path)
    current_heading = "Inici"
    current_chunk = []
    chunk_start_line = 1

    for line_idx, line in enumerate(lines, 1):
        if line.startswith("#+title:") or line.startswith("#+TITLE:"):
            title = line.split(":", 1)[1].strip()
        elif line.startswith("# ") and line_idx < 5:
            title = line[2:].strip()

        is_org_heading = line.startswith("*") and not line.startswith("#+") and len(line.split(" ")[0]) <= 4
        is_md_heading = line.startswith("#") and not line.startswith("#+") and len(line.split(" ")[0]) <= 4

        if (is_org_heading or is_md_heading) and current_chunk:
            text = "".join(current_chunk).strip()
            if len(text) > 30:
                chunks.append({
                    "start_line": chunk_start_line,
                    "heading": current_heading,
                    "content": text
                })
            current_chunk = []
            current_heading = line.strip()
            chunk_start_line = line_idx
        
        current_chunk.append(line)

        if len("".join(current_chunk)) > 1200:
            text = "".join(current_chunk).strip()
            if len(text) > 30:
                chunks.append({
                    "start_line": chunk_start_line,
                    "heading": current_heading,
                    "content": text
                })
            current_chunk = []
            chunk_start_line = line_idx + 1

    if current_chunk:
        text = "".join(current_chunk).strip()
        if len(text) > 30:
            chunks.append({
                "start_line": chunk_start_line,
                "heading": current_heading,
                "content": text
            })

    return title, chunks

# -------------------------------------------------------------
# 3. HIGH-SPEED BATCH VECTOR INDEXER
# -------------------------------------------------------------
def sync_index(force_rebuild=False):
    from fastembed import TextEmbedding
    model = TextEmbedding(model_name=MODEL_NAME)
    conn = get_db()

    if force_rebuild:
        conn.execute("DELETE FROM chunks;")
        conn.execute("DELETE FROM files;")
        conn.commit()

    all_files = []
    for ext in ('.org', '.md', '.qmd', '.txt'):
        all_files.extend(glob.glob(f"{BASE_DIR}/**/*{ext}", recursive=True))

    target_files = [
        f for f in all_files 
        if '/.git/' not in f and '/.system_generated/' not in f and '/.cache/' not in f and '/brain/' not in f
    ]

    indexed_count = 0
    updated_count = 0
    skipped_count = 0

    # Collect chunks needing embedding in batches
    for fpath in target_files:
        try:
            mtime = os.path.getmtime(fpath)
            with open(fpath, 'rb') as fp:
                chash = hashlib.sha256(fp.read()).hexdigest()
        except Exception:
            continue

        cur = conn.cursor()
        cur.execute("SELECT mtime, content_hash FROM files WHERE file_path = ?", (fpath,))
        row = cur.fetchone()

        if row and row[1] == chash and not force_rebuild:
            skipped_count += 1
            continue

        title, chunks = parse_and_chunk_file(fpath)
        if not chunks:
            continue

        conn.execute("DELETE FROM chunks WHERE file_path = ?", (fpath,))
        conn.execute("DELETE FROM files WHERE file_path = ?", (fpath,))

        texts_to_embed = [f"{title} | {c['heading']}\n{c['content']}" for c in chunks]
        embeddings = list(model.embed(texts_to_embed, batch_size=32))

        f_type = os.path.splitext(fpath)[1].replace('.', '')
        cur.execute(
            "INSERT INTO files (file_path, file_type, mtime, content_hash, title) VALUES (?, ?, ?, ?, ?)",
            (fpath, f_type, mtime, chash, title)
        )

        for idx, (c, emb) in enumerate(zip(chunks, embeddings)):
            emb_blob = np.array(emb, dtype=np.float32).tobytes()
            cur.execute(
                "INSERT INTO chunks (file_path, chunk_index, start_line, heading, content, embedding) VALUES (?, ?, ?, ?, ?, ?)",
                (fpath, idx, c['start_line'], c['heading'], c['content'], emb_blob)
            )

        conn.commit()
        if row:
            updated_count += 1
        else:
            indexed_count += 1

    conn.close()

    return {
        "status": "success",
        "total_files_monitored": len(target_files),
        "nous_fitxers_indexats": indexed_count,
        "fitxers_actualitzats": updated_count,
        "fitxers_sense_canvis": skipped_count
    }

# -------------------------------------------------------------
# 4. SEMANTIC SEARCH ENGINE
# -------------------------------------------------------------
def semantic_search(query, scope="all", top_k=5):
    from fastembed import TextEmbedding
    model = TextEmbedding(model_name=MODEL_NAME)
    conn = get_db()
    cur = conn.cursor()

    query_sql = "SELECT c.id, c.file_path, c.start_line, c.heading, c.content, c.embedding, f.title FROM chunks c JOIN files f ON c.file_path = f.file_path"
    params = []

    if scope == "notes":
        query_sql += " WHERE c.file_path LIKE ?"
        params.append(f"{BASE_DIR}/Notes/%")
    elif scope == "tfm":
        query_sql += " WHERE c.file_path LIKE ?"
        params.append(f"{BASE_DIR}/TFM/%")

    cur.execute(query_sql, params)
    rows = cur.fetchall()

    if not rows:
        sync_index()
        cur.execute(query_sql, params)
        rows = cur.fetchall()

    if not rows:
        return {"consulta": query, "resultats": []}

    q_vec = list(model.embed([query]))[0]
    q_norm = np.linalg.norm(q_vec)

    results = []
    for r in rows:
        cid, fpath, start_line, heading, content, emb_blob, title = r
        d_vec = np.frombuffer(emb_blob, dtype=np.float32)
        d_norm = np.linalg.norm(d_vec)
        
        sim = float(np.dot(q_vec, d_vec) / (q_norm * d_norm)) if q_norm and d_norm else 0.0

        results.append({
            "titol": title,
            "fitxer": os.path.basename(fpath),
            "ruta_completa": fpath,
            "enllaç": f"file://{fpath}#L{start_line}",
            "linia": start_line,
            "seccio": heading,
            "similitud": f"{sim * 100:.1f}%",
            "similitud_num": sim,
            "fragment": content[:260] + "..." if len(content) > 260 else content
        })

    results.sort(key=lambda x: x["similitud_num"], reverse=True)
    top_results = results[:top_k]

    conn.close()

    return {
        "consulta": query,
        "ambit": scope,
        "total_coincidencies": len(top_results),
        "resultats": top_results
    }

# -------------------------------------------------------------
# 5. FIND RELATED NOTES (Smart Backlinks)
# -------------------------------------------------------------
def find_related_notes(file_path, top_k=4):
    if not os.path.exists(file_path):
        return {"error": f"El fitxer '{file_path}' no existeix"}
    
    title, chunks = parse_and_chunk_file(file_path)
    if not chunks:
        return {"titol": title, "relacionats": []}
        
    full_text = " ".join([c["content"] for c in chunks[:3]])
    search_res = semantic_search(full_text[:400], scope="all", top_k=top_k+2)
    
    related = [r for r in search_res["resultats"] if r["ruta_completa"] != file_path][:top_k]
    
    return {
        "fitxer_origen": os.path.basename(file_path),
        "titol_origen": title,
        "notes_relacionades": related
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "search":
            q = sys.argv[2] if len(sys.argv) > 2 else "bateria xiaomi"
            sc = sys.argv[3] if len(sys.argv) > 3 else "all"
            res = semantic_search(q, scope=sc)
            print(json.dumps(res, indent=2, ensure_ascii=False))
        elif cmd == "sync":
            rebuild = "--rebuild" in sys.argv
            res = sync_index(force_rebuild=rebuild)
            print(json.dumps(res, indent=2, ensure_ascii=False))
        elif cmd == "related":
            fp = sys.argv[2]
            res = find_related_notes(fp)
            print(json.dumps(res, indent=2, ensure_ascii=False))
