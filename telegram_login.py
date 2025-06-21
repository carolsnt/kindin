# telegram_login.py

from telethon.sync import TelegramClient

api_id = 26704300
api_hash = '2238a452df5a09821978e339391b048b'

# Cria o cliente com o nome da sessão
with TelegramClient('kindin_session', api_id, api_hash) as client:
    print("Login realizado com sucesso!")
