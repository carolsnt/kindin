# Banco de Dados — Kindin

> Referência: [../KINDIN_SPEC.md](../KINDIN_SPEC.md) — seção 7.

## Diagrama lógico

```
users
  ├── destinations (user_id → users.id)
  ├── searches (user_id → users.id)
  ├── share_links (created_by_user_id → users.id)
  ├── send_jobs (user_id → users.id)
  └── sources (added_by_user_id → users.id, nullable)

searches
  └── search_results (search_id → searches.id)
        ├── source_id → sources.id
        └── share_links (search_result_id → search_results.id)

send_jobs
  ├── destination_id → destinations.id
  └── send_job_items (job_id → send_jobs.id)
        └── search_result_id → search_results.id
```

## Tabelas

### users
| Coluna | Tipo | Notas |
|--------|------|-------|
| id | UUID PK | |
| telegram_id | BIGINT | UNIQUE NOT NULL |
| username | TEXT | nullable |
| first_name | TEXT | nullable |
| last_name | TEXT | nullable |
| photo_url | TEXT | nullable |
| created_at | TIMESTAMPTZ | |
| updated_at | TIMESTAMPTZ | |

### destinations
| Coluna | Tipo | Notas |
|--------|------|-------|
| id | UUID PK | |
| user_id | UUID FK | → users.id |
| type | TEXT | kindle_email \| email |
| value | TEXT | endereço e-mail |
| label | TEXT | nome amigável |
| is_default | BOOL | default false |
| verified_at | TIMESTAMPTZ | nullable |
| created_at | TIMESTAMPTZ | |
| updated_at | TIMESTAMPTZ | |

### sources
| Coluna | Tipo | Notas |
|--------|------|-------|
| id | UUID PK | |
| type | TEXT | telegram_channel \| telegram_group |
| telegram_chat_id | BIGINT | UNIQUE NOT NULL |
| name | TEXT | |
| is_active | BOOL | default true |
| added_by_user_id | UUID FK | → users.id, nullable |
| created_at | TIMESTAMPTZ | |

### searches
| Coluna | Tipo | Notas |
|--------|------|-------|
| id | UUID PK | |
| user_id | UUID FK | → users.id |
| query_title | TEXT | nullable |
| query_author | TEXT | nullable |
| query_format | TEXT | any\|epub\|mobi\|pdf |
| status | TEXT | running\|done\|failed\|canceled |
| created_at | TIMESTAMPTZ | |
| updated_at | TIMESTAMPTZ | |

### search_results
| Coluna | Tipo | Notas |
|--------|------|-------|
| id | UUID PK | |
| search_id | UUID FK | → searches.id |
| source_id | UUID FK | → sources.id |
| telegram_message_id | BIGINT | NOT NULL |
| telegram_file_id | TEXT | NOT NULL |
| filename | TEXT | |
| format | TEXT | epub\|mobi\|pdf\|other |
| file_size | BIGINT | nullable |
| title_raw | TEXT | nullable |
| author_raw | TEXT | nullable |
| sha256 | TEXT | nullable |
| created_at | TIMESTAMPTZ | |
| **UNIQUE** | | (search_id, source_id, telegram_message_id, telegram_file_id) |

### share_links
| Coluna | Tipo | Notas |
|--------|------|-------|
| id | UUID PK | |
| search_result_id | UUID FK | → search_results.id |
| created_by_user_id | UUID FK | → users.id |
| token | TEXT | UNIQUE NOT NULL |
| expires_at | TIMESTAMPTZ | NOT NULL |
| created_at | TIMESTAMPTZ | |

### send_jobs
| Coluna | Tipo | Notas |
|--------|------|-------|
| id | UUID PK | |
| user_id | UUID FK | → users.id |
| destination_id | UUID FK | → destinations.id |
| status | TEXT | queued\|processing\|sent\|failed |
| error_message | TEXT | nullable |
| created_at | TIMESTAMPTZ | |
| updated_at | TIMESTAMPTZ | |

### send_job_items
| Coluna | Tipo | Notas |
|--------|------|-------|
| id | UUID PK | |
| job_id | UUID FK | → send_jobs.id |
| search_result_id | UUID FK | → search_results.id |
| status | TEXT | queued\|sent\|failed |
| error_message | TEXT | nullable |
