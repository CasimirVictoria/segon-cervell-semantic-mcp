# mcp-server-segon-cervell-semantic 🧠📚

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-blue.svg)](https://modelcontextprotocol.io/)

Servidor sobirà i d'alt rendiment basat en el **Model Context Protocol (MCP)** per a la cerca semàntica multilingüe i RAG (*Retrieval-Augmented Generation*) d'alta densitat sobre repositoris de text pla (**Org-mode `.org`**, **Markdown `.md`**, **Quarto `.qmd`** i **`.txt`**).

---

## 🏗️ Arquitectura i Integració amb l'Ecosistema

Aquest servidor forma part d'una **Plataforma Sobirana de Gestió del Coneixement i IA Personal**. Interopera de manera modular i transparent amb la resta de servidors MCP i interfícies del sistema:

```
                  ┌─────────────────────────────────────┐
                  │          AGY-Bridge / PWA           │
                  │   (Mobile Hub & Speech-to-Text)    │
                  └──────────────────┬──────────────────┘
                                     │
                  ┌──────────────────┴──────────────────┐
                  │      AI Agent Engine / Ollama       │
                  └─┬─────────────────┬───────────────┬─┘
                    │                 │               │
  ┌─────────────────▼───┐  ┌──────────▼──────────┐  ┌─▼──────────────────┐
  │ segon-cervell-mcp   │  │ mcp-server-academic │  │ email-mcp          │
  │ (Semantic Memory)   │  │ (Dialnet/CSIC/Open) │  │ (Inbox & Backup)   │
  └─────────────────────┘  └─────────────────────┘  └────────────────────┘
```

- **Integració amb `agy-bridge`:** Permet realitzar consultes semàntiques parlades o escrites en llenguatge natural des de dispositius mòbils a través d'una xarxa privada WireGuard / Tailscale, obtenint respostes sintetitzades en pocs mil·lisegons.
- **Integració amb `email-mcp`:** Facilita la destil·lació bidireccional: els comunicats i acords rebuts per correu s'incorporen a les notes de text pla i s'indexen automàticament; alhora, les respostes formals es redacten recuperant el context històric de la memòria semàntica.
- **Integració amb `mcp-server-academic-spain`:** La literatura científica i acadèmica recuperada es destil·la en notes atòmiques de recerca que queden connectades conceptualment a l'espai vectorial.
- **Integració amb l'Entorn de Treball (`Emacs / Denote`):** Retorna enllaços directes amb número de línia (`file:///ruta/al/fitxer.org#L42`), permetent la navegació immediata i la creació d'enllaços creuats intel·ligents (*Zettelkasten smart backlinks*).

---

## 💡 Filosofia: El Principi de la Densitat d'Informació (Maximització Senyal/Soroll)

El disseny del sistema es fonamenta en la **Teoria de la Informació de Claude Shannon** i la cerca del màxim ràtio Senyal/Soroll (*SNR*):

```
┌─────────────────────────────────────────────────────────────┐
│ 📚 1. DOCUMENTS EN BRUT (Articles, Informes, Burocràcia)    │
│    • Milers de pàgines i baix senyal per token.             │
└──────────────────────────────┬──────────────────────────────┘
                               │ (Destil·lació prèvia d'idees clau)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 💎 2. NOTES ATÒMIQUES EN TEXT PLA (Org-mode / Markdown)     │
│    • Ràtio Senyal/Soroll màxim (alta densitat cognitiva).   │
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

## ⚠️ El Problema Detectat: La Ineficiència de la Força Bruta

En l'ecosistema actual predomina la tendència a injectar desenes de documents feixucs directament a la finestra de context dels models (*context bloat*). Això provoca:
1. **Col·lapse computacional:** Els models locals (7B-14B) s'alenteixen exponencialment quan han de processar desenes de milers de tokens irrellevants.
2. **Augment d'al·lucinacions:** Com més gran i dispers és el context no estructurat, més fàcilment es perden els detalls clau.
3. **Pèrdua de privacitat i despesa econòmica:** Dependència de servidors al núvol amb tarifes recurrents per volum de tokens.

La solució és **la destil·lació atòmica prèvia**: emmagatzemar només l'essència en text pla i recuperar exclusivament el fragment necessari mitjançant cerca vectorial precisa.

---

## ✨ Característiques Tècniques

- **Motor d'Embeddings:** `fastembed` amb model multilingüe `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`.
- **Acceleració de Càlcul:** `ONNX Runtime` optimitzat per a CPU (sense necessitat de GPU dedicada ni dependències feixugues de PyTorch).
- **Format de Base de Dades:** SQLite local en mode WAL (`~/.local/share/segon_cervell/semantic_index.db`).
- **Aprofitament de la Memòria RAM:** Optimitzat per al *Page Cache* del nucli de Linux (`vm.vfs_cache_pressure = 10`, `vm.swappiness = 10`), executant cerques en menys de 5 mil·lisegons.
- **Fragmentació (*Chunking*) Intel·ligent:** Detecció automàtica d'arbres jeràrquics d'Org-mode (`*`, `**`, `***`), encapçalaments de Markdown (`#`, `##`, `###`) i paràgrafs amb preservació de la línia exacta del fitxer font.
- **Sincronització Incremental Ultra-ràpida:** Comparació per marques de temps (*mtime*) i sumes criptogràfiques SHA-256 (temps de verificació: `< 0,05 segons`).

---

## 🛠️ Eines Disponibles (MCP Tools)

### 🔍 `semantic_search_notes`
Executa cerques semàntiques en llenguatge natural a través de l'espai vectorial multilingüe.
- **Paràmetres:**
  - `query` *(string)*: Text de cerca en llenguatge natural (suporta Valencià, Castellà i Anglès indistintament).
  - `scope` *(string, opcional)*: Àmbit de cerca (`'all'`, `'notes'`, `'tfm'`).
  - `top_k` *(integer, opcional)*: Nombre màxim de resultats a retornar (per defecte: 5).
- **Retorn:** Títol, fitxer font, enllaç directe `file:///...#L42`, línia d'inici, secció, percentatge de similitud i fragment de text.

### 🔄 `sync_semantic_index`
Indexa i actualitza de manera incremental els fitxers nous o modificats en lots (*batch size = 32*).
- **Paràmetres:**
  - `force_rebuild` *(boolean, opcional)*: Si és `true`, reconstrueix la base de dades vectorial des de zero.

### 🔗 `find_related_notes`
Donada una nota de text pla, calcula la seua afinitat semàntica i descobreix automàticament altres notes conceptualment relacionades al repositori (*Smart Backlinks / Zettelkasten*).
- **Paràmetres:**
  - `file_path` *(string)*: Ruta absoluta del fitxer a analitzar.
  - `top_k` *(integer, opcional)*: Nombre de notes relacionades a descobrir (per defecte: 4).

---

## 🚀 Requisits i Instal·lació

```bash
# Instal·lació de dependències lleugeres
pip install --break-system-packages fastembed numpy
```

---

## 📄 Llicència
Distribuït sota llicència MIT. Consulta el fitxer `LICENSE` per a més informació.
