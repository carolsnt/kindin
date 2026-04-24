"""Telethon client wrapper (stub)."""


class TelegramClient:
    """Wrapper around Telethon for searching Telegram sources.
    
    TODO: implementar conexão real com Telethon.
    """

    def __init__(self, session_path: str, api_id: int, api_hash: str) -> None:
        self.session_path = session_path
        self.api_id = api_id
        self.api_hash = api_hash

    async def search_source(self, chat_id: int, query: str, formats: list[str]) -> list[dict]:
        """Search a Telegram source for book files (stub)."""
        return []
