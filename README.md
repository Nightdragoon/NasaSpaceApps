# NASA Space Apps — Helios Biology Knowledge Engine

## 🚀 Project Overview

**Helios Biology Knowledge Engine** is a project developed for the NASA International Space Apps Challenge.  
Its mission is to create a knowledge engine for biological data relevant to space, enabling researchers, students, and space enthusiasts to query, explore, and visualize biological relationships under space‑related conditions.

### Why Helios?

- Space biology is critical to understanding how life adapts to microgravity, radiation, and other extreme environments.  
- Helios aims to aggregate, analyze, and present biological data (genes, proteins, interactions, pathways) in a way that is accessible and useful for space research.  
- The system is built to be modular, scalable, and extensible for future datasets and features.

## 🧱 Architecture & Components

| Component | Description |
|-----------|-------------|
| **Data Ingestion** | Modules to import datasets from public databases (NCBI, UniProt, NASA life sciences repositories) |
| **Data Model / Graph DB** | A graph-based structure (e.g. Neo4j, Blazegraph, or RDF triple store) to represent relationships |
| **Query Engine / API** | A REST or GraphQL API layer to serve user queries and computations |
| **Frontend / UI** | Web interface allowing users to search, filter, visualize graphs, and download results |
| **Visualization Module** | Graph visualization with tools like D3.js, Cytoscape.js, or custom visual tools |
| **Analysis Plugins** | Add‑ons for operations such as pathway enrichment, network centrality, comparative biology |

## 🛠️ Setup & Installation

### Prerequisites

- Python 3.8+  
- Node.js / npm (for frontend)  
- Graph database (e.g. Neo4j Community / Enterprise edition)  
- Docker & Docker Compose (recommended for local multi‑component setup)

### Local Setup

1. Clone the repository:  
   ```bash
   git clone https://github.com/your-org/helios‑bioengine.git
   cd helios‑bioengine
   ```

2. Configure environment variables:  
   Copy `.env.example` to `.env` and fill in credentials (e.g. database URL, API keys).

3. Launch services via Docker Compose:  
   ```bash
   docker-compose up --build
   ```

4. Access the app:  
   - Backend / API: `http://localhost:8000`  
   - Frontend UI: `http://localhost:3000`

## 🧪 Usage & Example Queries

- **Get a gene and its interacting partners**  
  ```
  GET /api/v1/gene/TP53
  ```

- **Find pathway enrichment for a list of proteins**  
  ```
  POST /api/v1/pathway/enrich  
  Body: { "proteins": ["TP53","BRCA1","EGFR"] }
  ```

- **Visualize subnetwork between two proteins**  
  ```
  GET /api/v1/network?from=TP53&to=MDM2
  ```

- **Download results**  
  Results are returned in JSON or CSV depending on `Accept` header (`application/json` or `text/csv`).

## 🧩 How It Was Born (Inspiration from the Video)

This project builds upon the concept shown in the NASA Space Apps video, *Helios Biology Knowledge Engine*, where the team envisioned a knowledge framework for biological insights in space environments. It encapsulates the ideas of data interoperability, graph representations, and interactive discovery. ([youtu.be](https://youtu.be/0VUjeT2T0aA?si=-rqgCaBamI4V81QW))

## 📈 Future Extensions & Roadmap

- **Support for time‑series / longitudinal data** (e.g. gene expression over time in space)  
- **Machine learning / predictive modeling** for stress / adaptation signatures  
- **User annotation & community curation features**  
- **Interoperability with NASA APIs and space mission datasets**  
- **Mobile / offline UI version for researchers in remote labs**

## 🧑‍💻 Contributors & Team

- Emmannuel — Lead Backend / Data  
- Jacky — Lead Frontend / Viz  
- Brandon Almanza — Data Engineering & Integration  
- Aron — DevOps & Deployment
- Sarahi — DevOps & Deployment  

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
