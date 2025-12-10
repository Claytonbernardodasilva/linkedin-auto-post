# app/scheduler.py

import logging
import os
import random
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler  # type: ignore
from apscheduler.triggers.cron import CronTrigger

from dotenv import load_dotenv  # type: ignore
from openai import OpenAI  # type: ignore

from app.linkedin_api import publicar_post  # type: ignore


# ==============================
# 🔧 Carrega variáveis de ambiente
# ==============================
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=env_path)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()


# ==============================
# 📌 INTRO FIXA DO POST
# ==============================
INTRO = (
    "Olá sou Jarvis, a IA criada pelo Clayton Silva. "
    "A cada dia estarei postando conteúdos de Tecnologia e Inteligência Artificial."
)


# ==============================
# ✨ HINT DE ESTILO
# ==============================
STYLE_HINT = (
    "Mantenha 80–160 palavras, tom profissional e direto, focado em valor de negócio/carreira. "
    "Evite jargão excessivo. Use 5–8 emojis no máximo. Inclua um CTA claro em 1 frase. "
    "Inclua 6–8 hashtags na última linha. Português do Brasil."
)


# ==============================
# 🧠 PROMPTS POR TEMA
# Mantemos a chave 'recrutamento' para não quebrar o scheduler
# ==============================
PROMPTS_BY_TOPIC = {
    "recrutamento": [
        # 🔐 Segurança & APIs
        "Escreva um post (pt-BR) explicando boas práticas de segurança em APIs: autenticação com API Keys/OAuth2, rotação de segredos, IP allowlist e logs de auditoria. Traga 3 passos rápidos que qualquer empresa pode aplicar hoje.",
        "Crie um post (pt-BR) sobre como assinar e validar webhooks com HMAC (SHA-256): por que importa, como calcular a assinatura e como evitar ataques de replay. Inclua um mini checklist simples.",
        "Escreva um post (pt-BR) sobre rate limit em APIs: código 429, Retry-After, backoff exponencial e circuit breaker. Mostre um exemplo de política por plano Free/Pro/Enterprise.",

        # ⚙️ DevOps / Cloud
        "Crie um post (pt-BR) com um roteiro mínimo e realista de CI/CD para projetos Python/Node: testes, lint, build, secrets e deploy. Inclua 3 dicas práticas de GitHub Actions.",
        "Escreva um post (pt-BR) explicando containers vs. VMs e um passo a passo para dockerizar um serviço web simples. Acrescente os erros mais comuns para evitar.",
        "Crie um post (pt-BR) sobre observabilidade moderna: métricas, logs estruturados, tracing distribuído e dashboards. Traga 3 KPIs essenciais para times enxutos.",
        "Escreva um post (pt-BR) com 5 práticas de redução de custos em cloud: rightsizing, autoscaling, lifecycle de storage, reserved/spot e observabilidade de custo.",

        # 🧠 IA aplicada
        "Crie um post (pt-BR) sobre como escrever prompts eficazes para LLMs: contexto, objetivo, restrições e formato de saída. Inclua um template pronto para uso.",
        "Escreva um post (pt-BR) explicando RAG (Retrieval-Augmented Generation): quando usar, benefícios reais e um fluxo básico de implantação.",
        "Crie um post (pt-BR) comparando fine-tuning vs. prompt engineering vs. RAG: vantagens, limitações e quando escolher cada um.",
        "Escreva um post (pt-BR) sobre avaliação de respostas de IA: precisão factual, utilidade, segurança e métricas práticas para o dia a dia.",

        # 🗄️ Dados & Analytics
        "Crie um post (pt-BR) explicando as camadas Bronze/Silver/Gold no lakehouse e como isso simplifica qualidade e governança de dados.",
        "Escreva um post (pt-BR) com 7 dicas para SQL performático: índices, filtros seletivos, evitar SELECT *, CTEs com parcimônia e análise de planos.",
        "Crie um post (pt-BR) sobre Data Governance para times pequenos: catálogo de dados, linhagem, políticas de acesso e auditoria contínua.",
        "Escreva um post (pt-BR) explicando feature flags em produtos de dados: rollout progressivo, variantes A/B e auditoria de decisões.",

        # 🧩 Integrações & Automação
        "Crie um post (pt-BR) sobre quando usar n8n/Make para automações vs. construir integrações sob medida. Traga 3 critérios de decisão prática.",
        "Escreva um post (pt-BR) com um fluxo completo webhook → validação → fila → processamento assíncrono → callback. Explique por que o ACK <1s é obrigatório.",
        "Crie um post (pt-BR) sobre idempotência em operações de escrita: o que é, como implementar com Idempotency-Key + TTL e evitar duplicidade.",

        # 🛡️ Privacidade & LGPD
        "Escreva um post (pt-BR) com um checklist LGPD para times comerciais: base legal, consentimento, minimização, retenção e direitos do titular.",
        "Crie um post (pt-BR) explicando anonimização vs. pseudonimização com exemplos reais de quando usar cada uma.",
        "Escreva um post (pt-BR) sobre como preparar um DPA (contrato de operador) com fornecedores de dados e APIs. Traga 3 cláusulas críticas.",

        # 🧰 Engenharia de Software
        "Crie um post (pt-BR) sobre boas práticas de arquitetura em FastAPI/Laravel para APIs públicas: versionamento, validação de payload e erros padronizados.",
        "Escreva um post (pt-BR) com dicas de testes modernos: pirâmide de testes, mocks externos e testes de contrato de API.",
        "Crie um post (pt-BR) sobre cache inteligente: ETag, If-None-Match, TTL e invalidação. Inclua exemplos de quando NÃO usar cache.",

        # 📊 Produto
        "Escreva um post (pt-BR) explicando métricas de produto para APIs: adoção, TTFHW, erros 4xx/5xx e stickiness.",
        "Crie um post (pt-BR) sobre como publicar uma OpenAPI de forma amigável: exemplos claros, SDKs, sandbox e changelog sem fricção.",
        "Escreva um post (pt-BR) com 5 ideias de carrossel sobre TI/IA que geram alto dwell time.",

        # 🧪 Qualidade
        "Crie um post (pt-BR) sobre SLOs e SLAs para APIs: disponibilidade mensal, latência P95 e crédito por violação.",
        "Escreva um post (pt-BR) explicando estratégias de retries: jitter, limites, idempotência.",
        "Crie um post (pt-BR) sobre testes de resiliência: timeouts, chaos engineering leve e simulação de falhas.",

        # 🧭 Estratégia
        "Escreva um post (pt-BR) com 4 passos para medir ROI de iniciativas de dados/IA.",
        "Crie um post (pt-BR) sobre custos ocultos de integrações com terceiros.",

        # 🧑‍💻 UX & IA
        "Escreva um post (pt-BR) sobre como desenhar UX para funcionalidades com IA: transparência, edição, fallback.",
        "Crie um post (pt-BR) explicando detecção de alucinações em LLMs.",

        # 🔄 Operações
        "Escreva um post (pt-BR) sobre governança de mudanças em APIs.",
        "Crie um post (pt-BR) com um plano simples de resposta a incidentes.",
        "Escreva um post (pt-BR) explicando como monitorar consumo por chave/cliente."
    ]
}


# ==============================
# 🤖 Função que gera o texto
# ==============================
def gerar_texto_ia(topic: str) -> str:
    prompts = PROMPTS_BY_TOPIC.get(topic, [])
    if not prompts:
        prompts = ["Escreva um post breve (pt-BR) com uma dica prática de tecnologia."]

    prompt = random.choice(prompts) + " " + STYLE_HINT

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é um copywriter especializado em posts de tecnologia."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.9
        )

        corpo = (response.choices[0].message.content or "").strip()

        if "techinsightsconsult.com" not in corpo:
            corpo += "\n\n🌐 Saiba mais em: https://www.techinsightsconsult.com/"

        texto = f"{INTRO}\n\n{corpo}"

        if len(texto) > 2900:
            texto = texto[:2897] + "…"

        return texto

    except Exception as e:
        logger.error(f"Erro ao gerar texto com IA ({topic}): {e}")
        return f"{INTRO}\n\n[Erro ao gerar conteúdo — {topic}]"


# ==============================
# 🚀 Função que publica no LinkedIn
# ==============================
def job_post_linkedin(topic: str):
    try:
        texto = gerar_texto_ia(topic)
        publicar_post(texto)
        logger.info(f"Post publicado com sucesso ({topic}).")
    except Exception as e:
        logger.error(f"Erro ao publicar post: {e}")


# ==============================
# 📅 Scheduler — 10h e 14h, seg–sex
# ==============================
def start_scheduler():
    scheduler.add_job(
        job_post_linkedin,
        trigger=CronTrigger(day_of_week="mon-fri", hour=10, minute=0),
        kwargs={'topic': 'recrutamento'},
        id='post_10'
    )

    scheduler.add_job(
        job_post_linkedin,
        trigger=CronTrigger(day_of_week="mon-fri", hour=14, minute=0),
        kwargs={'topic': 'recrutamento'},
        id='post_14'
    )

    scheduler.start()
    logger.info("Scheduler iniciado: posts às 10:00 e 14:00, de segunda a sexta.")
