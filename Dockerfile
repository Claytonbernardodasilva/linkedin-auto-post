FROM python:3.11-slim

# Diretório de trabalho dentro do container
WORKDIR /app

# Copia requirements e instala dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

# Porta padrão do Cloud Run
ENV PORT=8080

# Comando para iniciar a API
# ATENÇÃO: isso assume que existe um objeto `app` dentro de app/main.py (FastAPI ou similar)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
