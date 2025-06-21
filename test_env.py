from dotenv import load_dotenv
import os

load_dotenv()

print("EMAIL_KINDLE:", os.getenv("EMAIL_KINDLE"))
print("EMAIL_REMETENTE:", os.getenv("EMAIL_REMETENTE"))
print("SENHA_EMAIL:", os.getenv("SENHA_EMAIL"))
print("API_ID:", os.getenv("API_ID"))
print("API_HASH:", os.getenv("API_HASH"))
