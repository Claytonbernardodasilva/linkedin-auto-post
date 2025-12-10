from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "LinkedIn Auto Post backend online"}


@app.get("/run-once-test")
async def run_once_test():
    """
    Endpoint de teste só pra confirmar que a segunda rota aparece no Cloud Run.
    NÃO chama LinkedIn nem scheduler ainda.
    """
    return {"status": "ok", "info": "Rota /run-once-test está funcionando no Cloud Run"}
