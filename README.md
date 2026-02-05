# Manager assist

## Architecture

For a detailed overview of the system architecture, graph workflows, and component interactions, see [architecture.md](architecture.md).

## Quick Start

### Prerequisites

Before running the deployment script, copy the environment example files and configure them:

1. **Root directory**: Copy `env.example` to `.env` and provide the required values
2. **Frontend directory**: Copy `frontend/env.example` to `frontend/.env` and provide the required values

### Deployment

To deploy Cortex on Windows OS, simply run:

```powershell
.\start.ps1
```

This script will:
- Create a virtual environment
- Install dependencies
- Build the manager-chat image
- Start all Docker services

Once complete, the following services will be available:
- **LangGraph API**: http://localhost:8123
  - **API Docs**: http://localhost:8123/docs
  - **LangGraph Studio**: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:8123
- **Frontend**: http://localhost:3000
- **Milvus**: http://localhost:19530
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

### Managing Services

View logs:
```powershell
docker-compose logs -f
```

Stop services:
```powershell
docker-compose down
```


# 🧠 Cortex: The Intelligent Memory Layer

**Cortex** is a next-generation AI assistant designed to function as a "Second Brain." Built on a sophisticated multi-agent architecture, it doesn't just store information—it understands, organizes, and verifies it to ensure you never lose a detail again.

---

## 🚀 Key Value Propositions

* **Adaptive Memory:** Automatically decides whether to store information as a structured fact (like a date or ID) or a conceptual memory (like a meeting summary).
* **Fact-Checked Responses:** Unlike standard AI that might "hallucinate," Cortex uses a self-correcting retrieval loop to verify its answers against your data.
* **Web-Enhanced Intelligence:** If the answer isn't in your personal notes, Cortex can securely bridge the gap by searching the web to provide full context.
* **Seamless Organization:** No more tagging or folder management. Just tell Cortex what to remember, and it handles the categorization.

---

## 🛠 Features & Capabilities

### 1. Intent-Aware Processing
Cortex uses an **Intelligence Router** to instantly classify your needs. Whether you are "depositing" a new memory or "withdrawing" an old one, the system optimizes the workflow in real-time.

### 2. Dual-Engine Storage
We utilize a hybrid storage strategy to ensure 100% recall accuracy:
* **Structured Storage (PostgreSQL):** For hard facts, dates, and specific data points.
* **Vector Memory (Milvus):** For semantic search, allowing you to find information based on "meanings" even if you forget the exact keywords.

### 3. Agentic RAG (Retrieval-Augmented Generation)
Our retrieval system acts like a digital researcher:
1.  **Search:** It scans your private database.
2.  **Grade:** It evaluates if the found information is actually relevant.
3.  **Verify:** It runs a "Hallucination Check" to ensure the final answer is grounded in reality.
4.  **Supplement:** If the data is missing, it performs a targeted Web Search.

---

## 💼 Ideal Use Cases

| User Type | Scenario |
| :--- | :--- |
| **Project Managers** | "What were the three blockers Sarah mentioned in the standup three weeks ago?" |
| **Executives** | "Summarize my last five interactions with the Board regarding the budget." |
| **Researchers** | "Cross-reference my internal notes on AI with the latest 2026 industry news." |
| **Personal Use** | "What is the Wi-Fi password for the guest house I stayed at last summer?" |

---

## 🏗 Technology Stack
Cortex is built on a robust, enterprise-grade foundation:
* **Orchestration:** LangGraph (Multi-agent coordination)
* **Logic:** LangChain & State-of-the-Art LLMs
* **Databases:** PostgreSQL (Relational) & Milvus (Vector)
* **Reliability:** Redis Caching & Docker Containerization

---

> **"Cortex isn't just an assistant; it's a cognitive upgrade. Stop searching for information and start using it."**
