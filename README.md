# 🧠 Segon Cervell Semantic Search MCP (`segon-cervell-semantic`)

Servidor **Model Context Protocol (MCP)** sobirà i local per a la cerca semàntica multilingüe i RAG (*Retrieval-Augmented Generation*) sobre el **Segon Cervell (`~/Documents/Segon_Cervell/`)**.

Dissenyat per a indexar i connectar notes de **Denote (`.org`, `.md`)**, capítols del **TFM (`.qmd`)**, documents de recerca i tasques en text pla a la velocitat del pensament, sense enviar mai dades a cap núvol extern.

---

## 🏛️ Arquitectura i Característiques

- **Motor d'Embeddings:** `fastembed` amb model multilingüe `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`.
- **Acceleració:** `ONNX Runtime` executat a la CPU (sense requerir GPU ni dependències de PyTorch).
- **Format de Base de Dades:** SQLite local (`~/.local/share/segon_cervell/semantic_index.db`).
- **Suport Multilingüe:** Cerca encreuada en **Valencià/Català, Castellà i Anglès**.
- **Chunking Intel·ligent:** Fragmentació automàtica per encapçalaments d'Org-mode (`*`, `**`, `***`), Markdown (`#`, `##`, `###`) i paràgrafs amb preservació del número de línia.
- **Sincronització Incremental:** Utilitza sumes de verificació SHA-256 i marques de temps (*mtime*); si els fitxers no han canviat, la comprovació triga menys de `0,05 segons`.

---

## 🛠️ Eines Disponibles (MCP Tools)

### 1. `semantic_search_notes`
Executa cerques semàntiques en llenguatge natural.
- **Paràmetres:**
  - `query` *(string)*: Text o pregunta de cerca (ex: *"com desactivar telemetria al mòbil"*, *"beques educatives NESE"*).
  - `scope` *(string, opcional)*: `'all'` (tot el Segon Cervell), `'notes'` (només Denote), `'tfm'` (només TFM).
  - `top_k` *(integer, opcional)*: Nombre de resultats a retornar (per defecte: 5).
- **Retorn:** Títol, fitxer, enllaç `file:///...#L42`, línia, secció, % de similitud i fragment de text.

### 2. `sync_semantic_index`
Indexa i actualitza de manera incremental tots els fitxers nous o modificats.
- **Paràmetres:**
  - `force_rebuild` *(boolean, opcional)*: Si és `true`, reconstrueix la base de dades vectorial des de zero.

### 3. `find_related_notes`
Analitza una nota existent i troba automàticament quines altres notes del Segon Cervell hi estan relacionades conceptualment (Zettelkasten / Smart Backlinks).
- **Paràmetres:**
  - `file_path` *(string)*: Ruta absoluta del fitxer a analitzar.
  - `top_k` *(integer, opcional)*: Nombre de notes relacionades a descobrir.

---

## 🚀 Requisits i Instal·lació

```bash
# Instal·lació de dependències
pip install --break-system-packages fastembed numpy
```

---

## 📄 Llicència
Projecte d'ús personal sobirà per al Segon Cervell de Casimir Victoria.
