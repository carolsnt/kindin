# Segurança — Kindin

> Referência: [../KINDIN_SPEC.md](../KINDIN_SPEC.md) — seção 6.

## Gate de fontes
- A busca ocorre **exclusivamente** em fontes com `is_active = true` na tabela `sources`.
- Somente administradores podem criar/editar fontes.
- Usuários comuns não têm acesso ao endpoint `POST /admin/sources`.

## Restrições de arquivo
- Extensões aceitas: `.epub`, `.mobi`, `.pdf`.
- Tamanho máximo configurável via `MAX_FILE_SIZE_MB` (padrão: 25 MB).
- Limite de resultados por busca configurável.
- Conteúdo nunca é executado; download é tratado como stream binário.

## Autenticação
- Login via **Telegram Login Widget**: hash validado com HMAC-SHA256 usando `SHA256(BOT_TOKEN)` como chave.
- Sessões gerenciadas com **JWT** (HS256), expiração configurável.
- Em `ENV=development`, a validação do hash é relaxada para facilitar desenvolvimento.

## Rate Limiting
- Rate limit por usuário (valores configuráveis via env):
  - Buscas por minuto: `RATE_LIMIT_SEARCHES_PER_MINUTE`
  - Downloads/envios por hora: `RATE_LIMIT_DOWNLOADS_PER_HOUR`
- Logs de auditoria registram ações sem expor segredos.

## Segredos
- Nunca commitar credenciais. Usar apenas `.env.example` como referência.
- Variáveis sensíveis: `JWT_SECRET`, `SMTP_PASS`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_API_HASH`, `DATABASE_URL`, `REDIS_URL`.
- Sessão do Telethon armazenada em arquivo protegido (`TELETHON_SESSION_PATH`) ou secret store.

## Futuro (pós-MVP)
- Integração com ClamAV para antivírus antes de disponibilizar share links e envios.
- Validação de MIME type além de extensão.
