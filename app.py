import re
import os
import asyncio
from flask import Flask, jsonify, render_template, request, abort
from telethon import TelegramClient
from telethon.tl.types import MessageMediaDocument
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

app = Flask(__name__)

# Configurações da API
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
api_token = os.getenv("API_TOKEN")  # Token da API para proteger a rota
session_name = "kindin_session"

# Página inicial com formulário
@app.route("/", methods=["GET", "POST"])
def home():
    mensagem = ''
    resultados = []
    if request.method == "POST":
        nome_livro = request.form.get("nome_livro", "").lower().strip()

        # Validação básica
        if len(nome_livro) > 100:
            abort(400, "Nome do livro muito longo.")

        # Sanitização da entrada (remove tudo que não é letra, número, espaço ou hífen)
        nome_livro = re.sub(r"[^\w\s\-]", "", nome_livro)

        # Executa a busca
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        epubs = loop.run_until_complete(buscar_epubs_telegram())
        resultados = [r for r in epubs if nome_livro in r["arquivo"].lower()]

        if resultados:
            mensagem = f'Foram encontrados {len(resultados)} arquivo(s) com "{nome_livro}".'
        else:
            mensagem = f'Nenhum arquivo encontrado para "{nome_livro}".'

    return render_template("index.html", mensagem=mensagem, resultados=resultados)

# Rota protegida por token para retornar JSON
@app.route("/buscar_epubs")
def buscar_epubs():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        abort(401, "Token não fornecido")

    token = auth_header.split(" ")[1]
    if token != api_token:
        abort(403, "Token inválido")

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    resultados = loop.run_until_complete(buscar_epubs_telegram())
    return jsonify(resultados)

# Função que busca arquivos EPUB no Telegram
async def buscar_epubs_telegram():
    resultados = []
    async with TelegramClient(session_name, api_id, api_hash) as client:
        async for dialog in client.iter_dialogs():
            if dialog.is_group or dialog.is_channel:
                async for message in client.iter_messages(dialog.id, limit=30):
                    if (
                        isinstance(message.media, MessageMediaDocument)
                        and message.file
                        and message.file.name
                        and message.file.name.endswith(".epub")
                        and message.media.document.mime_type == "application/epub+zip"
                    ):
                        resultados.append({
                            "chat": dialog.name,
                            "arquivo": message.file.name,
                            "mensagem_id": message.id,
                            "link": f"https://t.me/c/{str(dialog.id)[4:]}/{message.id}" if str(dialog.id).startswith("-100") else None
                        })
    return resultados

# Define cabeçalhos de segurança
@app.after_request
def set_security_headers(response):
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    return response

# Roda o servidor local
if __name__ == "__main__":
    app.run(debug=True)