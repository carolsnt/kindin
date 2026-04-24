# Kindin

Kindin é um app web para buscar livros (EPUB/MOBI/PDF) em fontes Telegram allowlisted, listar resultados em tempo real (SSE), e permitir enviar ao Kindle por e-mail, compartilhar e baixar. Login obrigatório via Telegram.

## Stack
- **Backend**: FastAPI + SQLAlchemy 2.0 + Alembic + PostgreSQL + Redis + Celery + Telethon
- **Frontend**: Next.js 14 + TailwindCSS + TypeScript

## Como rodar localmente

```bash
# Subir Postgres e Redis
docker compose -f infra/docker-compose.yml up -d postgres redis

# API
cd apps/api
pip install -e ".[dev]"
uvicorn kindin_api.main:app --reload

# Web
cd apps/web
npm install
npm run dev
```

## Documentação
- [Especificação completa](KINDIN_SPEC.md)
- [Arquitetura](docs/architecture.md)
- [Banco de dados](docs/database.md)
- [Segurança](docs/security.md)
- [API](docs/api.md)
