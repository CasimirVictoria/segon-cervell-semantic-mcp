# Segon Cervell Semantic Search MCP (`segon-cervell-semantic`)

Sovereign, local multilingual semantic search engine and RAG vector store for Casimir's Second Brain (`~/Documents/Segon_Cervell/`).

## Architecture

- **Embedding Engine:** FastEmbed with ONNX Runtime (`sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`).
- **Vector Storage:** Local SQLite database at `~/.local/share/segon_cervell/semantic_index.db`.
- **Supported Formats:** Org-mode (`.org`), Markdown (`.md`), Quarto (`.qmd`), Plain text (`.txt`).
- **Granularity:** Automatic document chunking by headings (`*`, `**`, `#`, `##`) and paragraphs with line number preservation.

## Available Tools

1. `semantic_search_notes(query, scope="all|notes|tfm", top_k=5)`:
   - Performs natural language semantic search across Catalan, Spanish, and English.
   - Returns file title, file path, line number, similarity percentage, and section snippet.

2. `sync_semantic_index(force_rebuild=False)`:
   - Incrementally checks file modification times and SHA-256 hashes, indexing only new or modified files in milliseconds.

3. `find_related_notes(file_path, top_k=4)`:
   - Discovers conceptually closest notes for Zettelkasten smart backlinking.
