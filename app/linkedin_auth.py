# app/linkedin_auth.py
import os
import requests
import base64
import json
from fastapi import APIRouter
from dotenv import load_dotenv, set_key

# Carrega o .env
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=env_path)

router = APIRouter()

CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
REDIRECT_URI = os.getenv("LINKEDIN_REDIRECT_URI")

@router.get("/auth/start")
def start_auth():
    """
    Gera a URL de autorização com escopos openid, profile, email e w_member_social.
    """
    if not CLIENT_ID or not REDIRECT_URI:
        return {"error": "Variáveis de ambiente não carregadas."}
    auth_url = (
        "https://www.linkedin.com/oauth/v2/authorization"
        f"?response_type=code&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope=openid%20profile%20email%20w_member_social"
    )
    return {"authorization_url": auth_url}

@router.get("/auth/callback")
def auth_callback(code: str):
    """
    Recebe o code, troca por access_token e id_token, salva-os no .env e atualiza os.environ.
    Decodifica o id_token para obter o 'sub', que é o identificador do usuário (user_id).
    """
    token_url = "https://www.linkedin.com/oauth/v2/accessToken"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    response = requests.post(token_url, data=data)
    if response.status_code != 200:
        return {"error": response.text}

    token_data = response.json()
    access_token = token_data.get("access_token")
    id_token = token_data.get("id_token")

    # Salvar access_token no .env e no ambiente
    if access_token:
        set_key(env_path, "LINKEDIN_ACCESS_TOKEN", access_token)
        os.environ["LINKEDIN_ACCESS_TOKEN"] = access_token

    # Decodificar id_token para extrair o 'sub' (user_id)
    if id_token:
        try:
            header_b64, payload_b64, signature_b64 = id_token.split(".")
            payload_b64 += "=" * (-len(payload_b64) % 4)
            payload_bytes = base64.urlsafe_b64decode(payload_b64.encode("utf-8"))
            payload = json.loads(payload_bytes)
            user_id = payload.get("sub")
            if user_id:
                set_key(env_path, "LINKEDIN_USER_ID", user_id)
                os.environ["LINKEDIN_USER_ID"] = user_id
        except Exception:
            pass

    return {
        "message": "Access token obtido e salvo no .env com sucesso!",
        "access_token": access_token,
    }

@router.get("/auth/save-token")
def save_token_manually(token: str):
    """
    Permite salvar manualmente um access_token no .env e atualizar os.environ.
    """
    set_key(env_path, "LINKEDIN_ACCESS_TOKEN", token)
    os.environ["LINKEDIN_ACCESS_TOKEN"] = token
    return {"message": "Token salvo com sucesso no .env"}

@router.get("/auth/test-token")
def test_token():
    """
    Apenas verifica se o access_token está presente.
    """
    access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    if not access_token:
        return {"error": "Nenhum access_token encontrado no .env"}
    return {"message": "Token presente. Pronto para postar!"}
