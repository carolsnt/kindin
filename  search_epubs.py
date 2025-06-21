from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaDocument
import os

# Substitua pelos seus próprios dados
api_id = 26704300
api_hash = '2238a452df5a09821978e339391b048b'
session_name = 'kindin_session'

# Nome do canal/grupo para buscar (você pode mudar ou deixar vazio e buscar globalmente)
search_query = '.epub'
max_messages = 100  # quantas mensagens buscar por vez

# Conectando com sua sessão salva
with TelegramClient(session_name, api_id, api_hash) as client:
    print("🔍 Buscando arquivos .epub...")

    count = 0
    for dialog in client.iter_dialogs():
        if dialog.is_group or dialog.is_channel:
            print(f"📂 Procurando em: {dialog.name}")
            for message in client.iter_messages(dialog.id, limit=max_messages):
                if message.media and isinstance(message.media, MessageMediaDocument):
                    if message.file and message.file.name and message.file.name.endswith(".epub"):
                        file_name = message.file.name
                        print(f"📥 Baixando: {file_name}")
                        path = client.download_media(message, file=file_name)
                        print(f"✅ Salvo em: {path}")
                        count += 1
    if count == 0:
        print("⚠️ Nenhum arquivo .epub encontrado.")
    else:
        print(f"🎉 Total de arquivos .epub baixados: {count}")
