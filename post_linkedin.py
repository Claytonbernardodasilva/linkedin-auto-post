# post_linkedin.py
import os
import requests
from dotenv import load_dotenv

# Carregar variáveis do .env
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=env_path)

ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")

def get_headers():
    if not ACCESS_TOKEN:
        raise Exception("Access token não encontrado. Gere com /auth/start e /auth/callback.")
    return {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }

def get_profile_urn():
    url = "https://api.linkedin.com/v2/me"
    response = requests.get(url, headers=get_headers())
    if response.status_code != 200:
        raise Exception(f"Erro ao obter perfil: {response.text}")
    data = response.json()
    return data.get("id")

def publicar_post(content: str):
    """
    Publica um post no LinkedIn.
    """
    profile_id = get_profile_urn()
    author_urn = f"urn:li:person:{profile_id}"

    url = "https://api.linkedin.com/v2/ugcPosts"
    payload = {
        "author": author_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": content},
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
    }

    response = requests.post(url, headers=get_headers(), json=payload)
    if response.status_code not in [200, 201]:
        raise Exception(f"Erro ao publicar post: {response.text}")
    return response.json()


if __name__ == "__main__":
    content = (
        "🚀 Tecnologia em Ação: Transformando ideias em soluções\n\n"
        "Quero compartilhar algumas experiências recentes aplicando Web, Dados e IA para impulsionar negócios e gerar inovação:\n\n"
        "🌐 Web Design Responsivo: Criação de sites modernos, com design limpo e foco em UX, garantindo presença online elegante e eficiente.\n\n"
        "📊 Dashboards no Power BI: Visualizações dinâmicas que transformam dados em insights acionáveis, facilitando decisões estratégicas em tempo real.\n\n"
        "🤖 Automação com Python e APIs: Scripts inteligentes para integrar sistemas, extrair dados e automatizar tarefas repetitivas, aumentando a produtividade.\n\n"
        "💬 IA Conversacional com LangChain: Chatbots avançados que entendem linguagem natural e fornecem respostas contextuais, otimizando processos e atendimentos.\n\n"
        "💡 Inspiração: A tecnologia amplifica resultados – de sites que atraem clientes, a dashboards que orientam decisões e IAs que conectam empresas e pessoas.\n\n"
        "🌟 Conheça mais em: techinsightsconsult.com\n\n"
        "#webdesign #powerbi #python #langchain #IA #automacao #inovacao #tecnologia"
    )

    print("Publicando post no LinkedIn...")
    result = publicar_post(content)
    print("Post publicado com sucesso!")
    print(result)
