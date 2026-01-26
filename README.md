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