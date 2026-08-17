# 🧠 Servidor MCP de Cerca Semàntica Sobirana per a Text Pla

Servidor **Model Context Protocol (MCP)** sobirà i local per a la cerca semàntica multilingüe i RAG (*Retrieval-Augmented Generation*) d'alta densitat cognitiva sobre repositoris de text pla (**Org-mode `.org`**, **Markdown `.md`**, **Quarto `.qmd`** i **`.txt`**).

---

## 🎯 1. Finalitat i Visió

La finalitat d'aquest projecte és transformar una col·lecció de notes i projectes de text pla en una **autèntica extensió cognitiva sobirana (Segon Cervell)**, permetent la recuperació instantània del coneixement per significat conceptual pur en lloc de dependre de noms de fitxer o paraules clau literals.

El sistema està concebut per a funcionar de manera **100% autònoma, local i privada**, optimitzat per a alimentar tant assistents avançats com **models locals d'intel·ligència artificial (com Qwen o Llama mitjançant Ollama)** amb el mínim consum computacional possible.

---

## ⚠️ 2. El Problema Detectat: La Ineficiència de la Força Bruta

En l'ecosistema actual de la IA i la gestió del coneixement, predomina un patró ineficient:

1. **Saturació del Context (*Context Bloat*):**  
   Intentar processar desenes de documents feixucs o llibres sencers en brut injecta centenars de milers de tokens de baix senyal (palla, introduccions, fórmules de cortesia i metadades) a la finestra de context del model.
2. **Col·lapse dels Models Locals:**  
   Els models d'IA locals executats a la CPU/GPU d'un ordinador personal (7B o 14B paràmetres) s'alenteixen dràsticament quan reben contextos massius, augmentant el temps de resposta i el consum d'energia.
3. **Dependència del Núvol i Pèrdua de Privacitat:**  
   Per a compensar la falta de síntesi, sovint es recorre a serveis al núvol amb costos recurrents i riscos de privacitat per a la informació personal i de recerca.

---

## 💡 3. La Solució Desenvolupada: La Llei de la Densitat d'Informació

Aquest MCP implementa una arquitectura basada en la **destil·lació prèvia del coneixement** i la **recuperació semàntica d'alta densitat**:

```
┌─────────────────────────────────────────────────────────────┐
│ 📚 1. DOCUMENTS EN BRUT (Articles, Informes, Burocràcia)    │
│    • Milers de pàgines i soroll contextual.                 │
└──────────────────────────────┬──────────────────────────────┘
                               │ (Destil·lació humana / recerca)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 💎 2. NOTES ATÒMIQUES EN TEXT PLA (Org-mode / Markdown)     │
│    • Ràtio Senyal/Soroll màxim (text dens i concís).        │
│    • Identificadors immutables i formats immortals.         │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ ⚡ 3. ÍNDEX SEMÀNTIC LOCAL (FastEmbed + SQLite a la RAM)    │
│    • Vectorització multilingüe (Valencià, Castellà, Anglès) │
│    • Cerca en 3 ms aprofitant el Page Cache de Linux.       │
└──────────────────────────────┬──────────────────────────────┘
                               │ (Només els 2 paràgrafs clau: ~100 tokens)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 🤖 4. ASSISTENT / MODEL LOCAL (Ollama / Qwen / Agents)      │
│    • Raonament instantani a 35+ tokens/segon a la CPU.      │
│    • Zero cost, zero APIs externes i privacitat total.      │
└─────────────────────────────────────────────────────────────┘
```

### 🤝 Eficiència i Divisió de Rols:
* **El gruix del treball quotidià (Memòria Viva & Coneixement Local):** Es resol de manera 100% autònoma i sobirana amb aquest MCP i models locals compactes (com Ollama / Qwen) a cost zero i màxima eficiència computacional.
* **Casos específics d'alta complexitat:** Reservant la intervenció de grans models de llenguatge (LLM) avançats únicament per a tasques puntuals que requerisquen una gran capacitat de síntesi o finestres de context extenses.

---

## 🏛️ 4. Arquitectura Tècnica

- **Motor d'Embeddings:** `fastembed` amb model multilingüe `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`.
- **Acceleració de Càlcul:** `ONNX Runtime` executat a la CPU (sense necessitat de GPU dedicada ni PyTorch feixuc).
- **Emmagatzematge Vectorial:** Base de dades SQLite local amb mode WAL (`~/.local/share/segon_cervell/semantic_index.db`).
- **Aprofitament de la Memòria RAM:** Optimitzat per a beneficiar-se del *Page Cache* del nucli de Linux (`vm.vfs_cache_pressure = 10`, `vm.swappiness = 10`), garantint cerques en pocs mil·lisegons.
- **Fragmentació (*Chunking*) Estructural:** Detecció automàtica d'arbres jeràrquics d'Org-mode (`*`, `**`, `***`), encapçalaments de Markdown (`#`, `##`, `###`) i paràgrafs amb preservació de la línia exacta del fitxer font.
- **Sincronització Incremental:** Verificació instantània mitjançant marques de temps (*mtime*) i hashes criptogràfics SHA-256 (temps de verificació: `< 0,05 segons`).

---

## 🛠️ 5. Eines Disponibles (MCP Tools)

### 🔍 `semantic_search_notes`
Executa cerques semàntiques en llenguatge natural a través de l'espai vectorial compartit.
- **Paràmetres:**
  - `query` *(string)*: Consulta en llenguatge natural (suporta Valencià, Castellà i Anglès indistintament).
  - `scope` *(string, opcional)*: Àmbit de cerca (`'all'`, `'notes'`, `'tfm'`).
  - `top_k` *(integer, opcional)*: Nombre màxim de resultats (per defecte: 5).
- **Retorn:** Títol, fitxer font, enllaç `file:///...#L42`, línia d'inici, secció, percentatge de similitud i fragment textual.

### 🔄 `sync_semantic_index`
Indexa i actualitza de manera incremental els fitxers nous o modificats en lots (*batch size = 32*).
- **Paràmetres:**
  - `force_rebuild` *(boolean, opcional)*: Si és `true`, reconstrueix la base de dades des de zero.

### 🔗 `find_related_notes`
Donada una nota de text pla, calcula la seua afinitat semàntica i descobreix automàticament altres notes conceptualment relacionades al repositori per a enllaços creuats (*Smart Backlinks / Zettelkasten*).
- **Paràmetres:**
  - `file_path` *(string)*: Ruta del fitxer a analitzar.
  - `top_k` *(integer, opcional)*: Nombre de notes relacionades a descobrir.

---

## 🚀 6. Requisits del Sistema

```bash
# Instal·lació de dependències lleugeres
pip install --break-system-packages fastembed numpy
```

---

## 📄 Llicència
Projecte lliure i sobirà de gestió del coneixement en text pla.
