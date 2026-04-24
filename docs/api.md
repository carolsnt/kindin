# Contratos da API — Kindin

> Referência: [../KINDIN_SPEC.md](../KINDIN_SPEC.md) — seções 8 e 9.

## Base URL
`/` (configurar `NEXT_PUBLIC_API_BASE_URL` no frontend)

## Autenticação
Todos os endpoints (exceto `/health`, `/auth/telegram` e `/s/{token}`) requerem header:
```
Authorization: Bearer <jwt_token>
```

## Endpoints

### Health
| Método | Path | Descrição |
|--------|------|-----------|
| GET | `/health` | Status da API |

### Auth
| Método | Path | Body | Resposta |
|--------|------|------|---------|
| POST | `/auth/telegram` | `TelegramAuthPayload` | `{ access_token, token_type, user_id }` |

### Destinos
| Método | Path | Descrição |
|--------|------|-----------|
| GET | `/me/destinations` | Listar destinos |
| POST | `/me/destinations` | Criar destino |
| PATCH | `/me/destinations/{id}` | Atualizar destino |
| DELETE | `/me/destinations/{id}` | Remover destino |

### Admin — Fontes
| Método | Path | Descrição |
|--------|------|-----------|
| GET | `/admin/sources` | Listar fontes |
| POST | `/admin/sources` | Criar fonte |
| PATCH | `/admin/sources/{id}` | Atualizar fonte |

### Buscas
| Método | Path | Body | Descrição |
|--------|------|------|-----------|
| POST | `/searches` | `{ title?, author?, format }` | Criar busca → `{ id }` |
| GET | `/searches/{id}/events` | — | SSE stream |
| GET | `/searches/{id}/results` | — | Resultados paginados |

### Download e Compartilhamento
| Método | Path | Descrição |
|--------|------|-----------|
| GET | `/downloads/results/{result_id}` | Download autenticado |
| POST | `/share-links` | Gerar link temporário |
| GET | `/s/{token}` | Download público via token |

### Envio
| Método | Path | Body | Descrição |
|--------|------|------|-----------|
| POST | `/send-jobs` | `{ destination_id, result_ids[] }` | Criar job de envio |
| GET | `/send-jobs/{job_id}` | — | Status do job |
| GET | `/send-jobs/{job_id}/items` | — | Itens do job |

## Eventos SSE (`GET /searches/{id}/events`)

| Tipo | Payload |
|------|---------|
| `progress` | `{ scanned_sources, total_sources, scanned_messages? }` |
| `result` | `{ result_id, filename, format, file_size?, title_raw?, author_raw? }` |
| `done` | `{ total_results }` |
| `error` | `{ message }` |
