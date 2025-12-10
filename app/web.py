from fastapi import FastAPI, HTTPException, Query

from app.scheduler import job_post_linkedin

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "LinkedIn Auto Post backend online"}


# ⚠️ Este endpoint REALMENTE posta no LinkedIn
# Exemplo de uso:
# GET /run-once          -> usa topic padrão "recrutamento"
# GET /run-once?topic=lgpd  -> usa outro tópico (se você criar no dict)
@app.get("/run-once")
async def run_once(topic: str = Query("recrutamento")):
    ok = job_post_linkedin(topic)
    if not ok:
        # Se der erro, devolve 500 pra você ver na resposta
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao publicar post no LinkedIn para o tópico '{topic}'. Veja os logs do Cloud Run."
        )
    return {"status": "ok", "topic": topic}

