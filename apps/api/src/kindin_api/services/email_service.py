"""SMTP e-mail service wrapper (stub)."""


class EmailService:
    """Wrapper around SMTP for sending books by e-mail.
    
    TODO: implementar envio real via smtplib/aiosmtplib.
    """

    def __init__(self, host: str, port: int, user: str, password: str, from_addr: str) -> None:
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.from_addr = from_addr

    async def send_file(self, to: str, subject: str, filename: str, content: bytes) -> bool:
        """Send a file via e-mail (stub)."""
        return False
