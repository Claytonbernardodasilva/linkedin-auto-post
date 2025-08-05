# app/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import os
from dotenv import load_dotenv
from app.linkedin_api import publicar_post  # type: ignore
from openai import OpenAI  # type: ignore
import random

# Carrega .env
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=env_path)

# Inicializa cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Configuração de logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cria o scheduler
scheduler = BackgroundScheduler()

# Lista de prompts (corrigida)
PROMPTS = [
    "Compartilhe um exemplo real de como a Inteligência Artificial está otimizando processos logísticos ou industriais. Use linguagem clara, emojis e finalize com: Descubra mais em https://www.techinsightsconsult.com/",
    "Escreva um post explicando como pequenas empresas também podem se beneficiar de IA com ferramentas acessíveis como Power Platform e automações Python. Inclua emojis e convite para visitar: https://www.techinsightsconsult.com/",
    "Crie um post abordando o impacto dos chatbots com IA no atendimento ao cliente. Dê um exemplo prático, use emojis e convide o leitor a saber mais em https://www.techinsightsconsult.com/",
    "Crie um post mostrando como a análise de dados pode revelar padrões ocultos que melhoram a tomada de decisão. Use um caso hipotético e finalize com: Saiba mais em https://www.techinsightsconsult.com/",
    "Escreva um post com 3 formas práticas de aplicar Data Science em setores como varejo, saúde ou finanças. Use exemplos simples, emojis e finalize com: Conheça mais em https://www.techinsightsconsult.com/",
    "Conte um caso fictício onde uma empresa usou dashboards em Power BI conectados com APIs para prever demandas. Inclua métricas e chame para conhecer https://www.techinsightsconsult.com/",
    "Compartilhe um post motivacional sobre como a tecnologia pode ser uma ponte para a reinvenção de carreira. Use emojis e finalize com: Inspire-se mais em https://www.techinsightsconsult.com/",
    "Escreva uma mensagem inspiradora para quem está começando na área de tecnologia. Fale sobre curiosidade, aprendizado contínuo e convide para visitar https://www.techinsightsconsult.com/",
    "Crie um post que fale sobre resiliência no ambiente profissional e como a mentalidade de inovação pode transformar obstáculos em oportunidades. Finalize com: Saiba mais em https://www.techinsightsconsult.com/",
    "Publique uma reflexão sobre como pequenas mudanças diárias com foco em melhoria contínua geram grandes impactos. Use emojis positivos e feche com: Explore novas ideias em https://www.techinsightsconsult.com/"
]

def gerar_texto_ia():
    prompt = random.choice(PROMPTS)
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        texto = response.choices[0].message.content.strip()

        if "techinsightsconsult.com" not in texto:
            texto += "\n\n🌐 Saiba mais em: https://www.techinsightsconsult.com/"

        if len(texto) > 2900:
            texto = texto[:2897] + "…"

        return texto
    except Exception as e:
        logger.error(f"Erro ao gerar texto com IA: {e}")
        return "Erro ao gerar conteúdo. 🌐 Saiba mais em https://www.techinsightsconsult.com/."

def job_post_linkedin():
    try:
        texto_post = gerar_texto_ia()
        logger.info(f"Texto gerado ({len(texto_post)} caracteres):\n{texto_post}")
        logger.info("Publicando post no LinkedIn...")
        publicar_post(texto_post)
        logger.info("Post publicado com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao publicar post: {e}")

def start_scheduler():
    scheduler.add_job(job_post_linkedin, 'interval', hours=1)
    scheduler.start()
    logger.info("Scheduler iniciado.")
