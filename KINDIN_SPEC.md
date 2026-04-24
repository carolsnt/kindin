# Kindin — Especificação Completa

## 1. Visão Geral

Kindin é um app web para buscar livros (EPUB/MOBI/PDF) em fontes Telegram allowlisted, listar resultados em tempo real (SSE), e permitir enviar ao Kindle por e-mail, compartilhar e baixar. Login obrigatório via Telegram.

## 2. Objetivos

- Permitir que usuários autenticados busquem livros em grupos/canais Telegram pré-aprovados.
- Listar resultados em tempo real via Server-Sent Events (SSE).
- Permitir baixar, compartilhar (link público temporário) e enviar arquivos por e-mail (Kindle ou qualquer e-mail).
- Interface web responsiva, simples e rápida.

## 3. Não-objetivos (MVP)

- Upload de arquivos pelo usuário.
- Conversão de formatos de e-book.
- Indexação permanente/crawler contínuo (busca é on-demand).
- Aplicativo mobile nativo.
- Multi-tenancy / múltiplos bots Telegram.

## 4. Stack Técnica

### Backend
- **FastAPI** (Python 3.11+)
- **SQLAlchemy 2.0** (ORM, síncrono no MVP)
- **Alembic** (migrations)
- **PostgreSQL 16** (banco de dados principal)
- **Redis 7** (broker Celery + cache)
- **Celery 5** (filas de tarefas assíncronas)
- **Telethon** (cliente MTProto para Telegram)
- **python-jose** (JWT)
- **pydantic-settings** (configuração via env)

### Frontend
- **Next.js 14** (App Router, TypeScript)
- **TailwindCSS 3**
- SSE nativo via `EventSource`

### Infraestrutura
- **Docker Compose** para desenvolvimento local
- **PostgreSQL** e **Redis** como serviços gerenciados

## 5. Arquitetura

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

### Fluxo de busca
1. Usuário submete formulário no frontend.
2. Frontend chama `POST /searches` → recebe `search_id`.
3. API cria registro `Search` e dispara task Celery `kindin.telegram_search`.
4. Frontend abre SSE em `GET /searches/{id}/events`.
5. Worker busca mensagens em fontes allowlisted via Telethon.
6. Worker publica eventos no Redis; API consome e envia via SSE.
7. Ao terminar, worker atualiza `Search.status = done`.
8. Frontend exibe resultados em tempo real.

## 6. Segurança

### Autenticação
- Login via **Telegram Login Widget** (HMAC-SHA256 com `SHA256(BOT_TOKEN)`).
- Sessões via **JWT** (HS256), expiração configurável.

### Autorização
- Busca ocorre exclusivamente em fontes `is_active = true`.
- Somente admins podem criar/editar fontes.

### Restrições de arquivo
- Extensões aceitas: `.epub`, `.mobi`, `.pdf`.
- Tamanho máximo: `MAX_FILE_SIZE_MB` (padrão 25 MB).
- Conteúdo nunca é executado.

### Rate Limiting
- Buscas por minuto: `RATE_LIMIT_SEARCHES_PER_MINUTE`.
- Downloads/envios por hora: `RATE_LIMIT_DOWNLOADS_PER_HOUR`.

## 7. Banco de Dados

### Tabelas principais

#### users
- `id` UUID PK
- `telegram_id` BIGINT UNIQUE NOT NULL
- `username`, `first_name`, `last_name`, `photo_url` TEXT nullable
- `created_at`, `updated_at` TIMESTAMPTZ

#### destinations
- `id` UUID PK
- `user_id` UUID FK → users
- `type` TEXT (kindle_email | email)
- `value` TEXT (endereço e-mail)
- `label` TEXT
- `is_default` BOOL
- `verified_at` TIMESTAMPTZ nullable
- `created_at`, `updated_at` TIMESTAMPTZ

#### sources
- `id` UUID PK
- `type` TEXT (telegram_channel | telegram_group)
- `telegram_chat_id` BIGINT UNIQUE NOT NULL
- `name` TEXT
- `is_active` BOOL default true
- `added_by_user_id` UUID FK → users nullable
- `created_at` TIMESTAMPTZ

#### searches
- `id` UUID PK
- `user_id` UUID FK → users
- `query_title`, `query_author` TEXT nullable
- `query_format` TEXT (any|epub|mobi|pdf)
- `status` TEXT (running|done|failed|canceled)
- `created_at`, `updated_at` TIMESTAMPTZ

#### search_results
- `id` UUID PK
- `search_id` UUID FK → searches
- `source_id` UUID FK → sources
- `telegram_message_id` BIGINT NOT NULL
- `telegram_file_id` TEXT NOT NULL
- `filename` TEXT
- `format` TEXT (epub|mobi|pdf|other)
- `file_size` BIGINT nullable
- `title_raw`, `author_raw`, `sha256` TEXT nullable
- `created_at` TIMESTAMPTZ
- UNIQUE (search_id, source_id, telegram_message_id, telegram_file_id)

#### share_links
- `id` UUID PK
- `search_result_id` UUID FK → search_results
- `created_by_user_id` UUID FK → users
- `token` TEXT UNIQUE NOT NULL
- `expires_at` TIMESTAMPTZ NOT NULL
- `created_at` TIMESTAMPTZ

#### send_jobs
- `id` UUID PK
- `user_id` UUID FK → users
- `destination_id` UUID FK → destinations
- `status` TEXT (queued|processing|sent|failed)
- `error_message` TEXT nullable
- `created_at`, `updated_at` TIMESTAMPTZ

#### send_job_items
- `id` UUID PK
- `job_id` UUID FK → send_jobs
- `search_result_id` UUID FK → search_results
- `status` TEXT (queued|sent|failed)
- `error_message` TEXT nullable

## 8. API REST

### Auth
- `POST /auth/telegram` — Valida Telegram Login Widget e retorna JWT.

### Destinos
- `GET /me/destinations` — Lista destinos do usuário.
- `POST /me/destinations` — Cria destino.
- `PATCH /me/destinations/{id}` — Atualiza destino.
- `DELETE /me/destinations/{id}` — Remove destino.

### Admin — Fontes
- `GET /admin/sources` — Lista fontes.
- `POST /admin/sources` — Cria fonte.
- `PATCH /admin/sources/{id}` — Atualiza fonte.

### Buscas
- `POST /searches` — Cria busca → `{ id, status, created_at }`.
- `GET /searches/{id}/events` — SSE stream de resultados.
- `GET /searches/{id}/results` — Resultados paginados.

### Download e Compartilhamento
- `GET /downloads/results/{result_id}` — Download autenticado.
- `POST /share-links` — Gera link temporário.
- `GET /s/{token}` — Download público via token.

### Envio
- `POST /send-jobs` — Cria job de envio `{ destination_id, result_ids[] }`.
- `GET /send-jobs/{job_id}` — Status do job.
- `GET /send-jobs/{job_id}/items` — Itens do job.

## 9. Eventos SSE

Endpoint: `GET /searches/{id}/events`

| Tipo | Payload |
|------|---------|
| `progress` | `{ scanned_sources, total_sources, scanned_messages? }` |
| `result` | `{ result_id, filename, format, file_size?, title_raw?, author_raw? }` |
| `done` | `{ total_results }` |
| `error` | `{ message }` |

## 10. Workers Celery

### kindin.telegram_search
- Recebe `search_id`.
- Para cada fonte ativa, usa Telethon para pesquisar mensagens com arquivos.
- Filtra por formato e tamanho.
- Persiste `SearchResult` e publica evento SSE via Redis.
- Atualiza `Search.status = done` ao terminar.

### kindin.email_sender
- Recebe `job_id`.
- Para cada item do job, baixa arquivo via Telethon.
- Envia por SMTP com anexo.
- Atualiza status do item e do job.

## 11. Frontend — Páginas

### `/` (Home)
- Formulário de busca: título, autor (opcional), formato.
- Após submit: chama `POST /searches`, redireciona para `/search/{id}`.

### `/search/{id}`
- Abre SSE em `/searches/{id}/events`.
- Lista resultados em tempo real.
- Cada item tem checkboxes e botões: Enviar, Compartilhar, Baixar.

### `/login`
- Telegram Login Widget.
- Armazena JWT no localStorage após autenticação.

### `/destinations`
- Lista, cria, edita e remove destinos de e-mail.

## 12. Configuração (env vars)

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| `DATABASE_URL` | postgresql+psycopg://... | URL do PostgreSQL |
| `REDIS_URL` | redis://localhost:6379/0 | URL do Redis |
| `JWT_SECRET` | changeme-supersecret | Segredo JWT |
| `JWT_ALGORITHM` | HS256 | Algoritmo JWT |
| `JWT_EXPIRE_MINUTES` | 10080 (7d) | Expiração do token |
| `SMTP_HOST` | smtp.example.com | Host SMTP |
| `SMTP_PORT` | 587 | Porta SMTP |
| `SMTP_USER` | | Usuário SMTP |
| `SMTP_PASS` | | Senha SMTP |
| `SMTP_FROM` | noreply@example.com | Remetente |
| `TELETHON_SESSION_PATH` | ./kindin.session | Caminho da sessão |
| `TELEGRAM_API_ID` | 0 | API ID do Telegram |
| `TELEGRAM_API_HASH` | | API Hash do Telegram |
| `TELEGRAM_BOT_TOKEN` | | Token do bot |
| `MAX_FILE_SIZE_MB` | 25 | Tamanho máximo (MB) |
| `SHARE_LINK_TTL_HOURS` | 24 | TTL dos share links |
| `RATE_LIMIT_SEARCHES_PER_MINUTE` | 10 | Rate limit buscas |
| `RATE_LIMIT_DOWNLOADS_PER_HOUR` | 50 | Rate limit downloads |
| `ENV` | development | Ambiente |

## 13. Como Rodar Localmente

```bash
# 1. Subir infraestrutura
docker compose -f infra/docker-compose.yml up -d postgres redis

# 2. API
cd apps/api
cp .env.example .env
pip install -e ".[dev]"
alembic upgrade head
uvicorn kindin_api.main:app --reload

# 3. Worker (outro terminal)
cd apps/api
celery -A kindin_api.workers.celery_app worker --loglevel=info

# 4. Frontend
cd apps/web
cp .env.example .env.local
npm install
npm run dev
```

## 14. CI/CD

GitHub Actions (`.github/workflows/ci.yml`):
- **api**: instala deps Python, roda pytest.
- **web**: instala deps Node, roda `next build`.

## 15. Estrutura de Diretórios

```
kindin/
├── apps/
│   ├── api/
│   │   ├── src/kindin_api/
│   │   │   ├── models/
│   │   │   ├── schemas/
│   │   │   ├── routers/
│   │   │   ├── workers/
│   │   │   └── services/
│   │   ├── alembic/
│   │   │   └── versions/
│   │   └── tests/
│   └── web/
│       └── src/
│           ├── app/
│           ├── components/
│           └── lib/
├── infra/
│   └── docker-compose.yml
├── docs/
└── .github/workflows/
```

## 16. Roadmap Pós-MVP

- Conversão automática de formato (e.g., MOBI → EPUB via Calibre).
- Indexação contínua em background para acelerar buscas.
- Antivírus (ClamAV) antes de disponibilizar downloads.
- Aplicativo mobile (React Native ou Flutter).
- Suporte a múltiplos bots Telegram.
- Dashboard de administração para gerenciar fontes e usuários.
- Notificações push quando o envio ao Kindle for concluído.
