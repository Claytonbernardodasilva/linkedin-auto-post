# app/linkedin_api.py
import os
import requests
from dotenv import load_dotenv

# Carrega o .env (define override=True para recarregar valores atualizados)
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=env_path, override=True)

def get_headers():
    """
    Monta cabeçalhos de autenticação para API do LinkedIn.
    """
    access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    if not access_token:
        raise Exception("Access token não encontrado. Execute /auth/start e /auth/callback.")
    return {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
    }

def get_profile_urn():
    """
    Lê o user_id (sub) do .env dinamicamente e forma a URN do autor.
    """
    # Recarrega o .env para garantir valores atualizados
    load_dotenv(dotenv_path=env_path, override=True)
    user_id = os.getenv("LINKEDIN_USER_ID")
    if not user_id:
        raise Exception("User ID não encontrado. Faça o fluxo de autenticação para decodificar o id_token.")
    return f"urn:li:person:{user_id}"

def publicar_post(content: str):
    """
    Publica um post de texto no LinkedIn usando UGC Posts API.
    """
    author_urn = get_profile_urn()
    url = "https://api.linkedin.com/v2/ugcPosts"
    payload = {
        "author": author_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": content},
                "shareMediaCategory": "NONE",
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        },
    }
    response = requests.post(url, headers=get_headers(), json=payload)
    if response.status_code not in (200, 201):
        raise Exception(f"Erro ao publicar post: {response.status_code} - {response.text}")
    return response.json()

def buscar_metricas(post_id: str):
    """
    Busca curtidas e comentários de um post já publicado.
    """
    url = f"https://api.linkedin.com/v2/socialActions/{post_id}"
    response = requests.get(url, headers=get_headers())
    if response.status_code != 200:
        raise Exception(f"Erro ao buscar métricas: {response.status_code} - {response.text}")
    return response.json()
