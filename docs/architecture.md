# Arquitetura do Kindin

> Referência: [../KINDIN_SPEC.md](../KINDIN_SPEC.md) — seções 5 e 10.

## Visão geral

```
[ Browser / Next.js ]
       |  HTTPS
       v
[ FastAPI (uvicorn) ]  <-->  [ PostgreSQL ]
       |                          |
       | Celery tasks             | SQLAlchemy 2.0
       v
[ Worker (Celery) ]  <-->  [ Redis (broker/backend) ]
       |
       | Telethon (MTProto)
       v
[ Telegram API ]
```

## Camadas

### Frontend (apps/web)
- **Next.js 14** com App Router e TypeScript.
- **TailwindCSS** para estilização responsiva.
- Recebe resultados de busca via **SSE** (`/searches/{id}/events`).
- Comunica-se com a API via `lib/api.ts`.

### API (apps/api)
- **FastAPI** com routers modulares por domínio.
- Autenticação via **Telegram Login Widget** + **JWT**.
- Acesso ao banco de dados via **SQLAlchemy 2.0** (síncrono no MVP).
- Endpoints SSE com `StreamingResponse` para streaming de resultados.

### Worker (Celery)
- Broker e backend: **Redis**.
- Tarefas:
  - `kindin.telegram_search`: varre fontes Telegram e persiste `search_results`.
  - `kindin.email_sender`: envia arquivos via SMTP.

### Banco de Dados (PostgreSQL)
- Todas as tabelas descritas na seção 7 da spec.
- Migrations gerenciadas por **Alembic**.

### Tempo real (SSE)
- O worker publica eventos no Redis; a API os consome e os envia ao cliente via SSE.
- Alternativa de fallback: `GET /searches/{id}/results` paginado.

### Telethon
- A sessão de usuário Telegram fica armazenada no servidor (`TELETHON_SESSION_PATH`).
- O worker usa Telethon para pesquisar mensagens em fontes allowlisted.
