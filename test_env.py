from dotenv import load_dotenv
import os

# Força o carregamento do .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

print("CLIENT_ID:", os.getenv("LINKEDIN_CLIENT_ID"))
print("SECRET:", os.getenv("LINKEDIN_CLIENT_SECRET"))
print("REDIRECT:", os.getenv("LINKEDIN_REDIRECT_URI"))

