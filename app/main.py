# app/main.py
from fastapi import FastAPI, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from .database import SessionLocal, init_db
from . import models, schemas
from .scheduler import start_scheduler
from .linkedin_auth import router as linkedin_auth_router
from .linkedin_api import publicar_post, buscar_metricas

# Cria instância do FastAPI
app = FastAPI(title="LinkedIn Auto Post")

# Inclui rotas de autenticação
app.include_router(linkedin_auth_router)

# Inicializa banco de dados (se houver) e scheduler
init_db()
start_scheduler()

# Sessão do banco de dados (exemplo)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rotas CRUD locais de exemplo
@app.post("/posts/", response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    db_post = models.Post(content=post.content)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@app.get("/posts/", response_model=list[schemas.Post])
def read_posts(db: Session = Depends(get_db)):
    return db.query(models.Post).all()

# Endpoint para publicar manualmente no LinkedIn
@app.post("/linkedin/post")
def create_linkedin_post(content: str = Body(..., embed=True)):
    try:
        response = publicar_post(content)
        return {"message": "Post criado com sucesso!", "response": response}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint para buscar métricas
@app.get("/linkedin/metrics/{post_id}")
def get_linkedin_metrics(post_id: str):
    try:
        metrics = buscar_metricas(post_id)
        return {"post_id": post_id, "metrics": metrics}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint para testar publicação com IA (sem esperar 1 hora)
@app.get("/test-post")
def test_post():
    try:
        from .scheduler import job_post_linkedin
        job_post_linkedin()  # dispara o job manualmente
        return {"message": "Post enviado com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
