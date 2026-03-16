from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from routers import heroes, auth
# Crear tablas automáticamente
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Marvel Heroes API",
    description="API para gestionar héroes de Marvel",
    version="1.0.1"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(heroes.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Marvel Heroes API running"}