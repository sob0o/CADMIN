from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import designs

app = FastAPI(title="CADMIN - Lattice Design Suite")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(designs.router)


@app.get("/health")
def health():
    return {"status": "ok"}