# test_openai.py
import os
from openai import OpenAI # type: ignore
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("Erro: OPENAI_API_KEY não encontrada no .env")
    exit(1)

# Inicializa cliente OpenAI
client = OpenAI(api_key=api_key)

try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Escreva uma frase de teste para confirmar que a API está funcionando."}],
        max_tokens=50
    )
    print("Resposta da OpenAI:")
    print(response.choices[0].message.content.strip())
except Exception as e:
    print(f"Erro ao testar a API da OpenAI: {e}")