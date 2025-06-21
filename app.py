from flask import Flask, jsonify
from telethon import TelegramClient
from telethon.tl.types import MessageMediaDocument
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session_name = "kindin_session"

@app.route("/")
def home():
    return """
    <h1>Prosa Tech - Cybertec para Divas</h1>
    <p>API ativa! Para buscar arquivos EPUB, acesse <a href='/buscar_epubs'>/buscar_epubs</a>.</p>
    """

async def buscar_epubs_telegram():
    resultados = []
    async with TelegramClient(session_name, api_id, api_hash) as client:
        async for dialog in client.iter_dialogs():
            if dialog.is_group or dialog.is_channel:
                async for message in client.iter_messages(dialog.id, limit=30):
                    if isinstance(message.media, MessageMediaDocument):
                        if message.file and message.file.name and message.file.name.endswith(".epub"):
                            resultados.append({
                                "chat": dialog.name,
                                "arquivo": message.file.name,
                                "mensagem_id": message.id,
                                "link": f"https://t.me/c/{str(dialog.id)[4:]}/{message.id}" if str(dialog.id).startswith("-100") else None
                            })
    return resultados

@app.route("/buscar_epubs")
def buscar_epubs():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    resultados = loop.run_until_complete(buscar_epubs_telegram())
    return jsonify(resultados)

if __name__ == "__main__":
    app.run(debug=True)
