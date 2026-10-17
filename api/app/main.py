from fastapi import FastAPI

from app.routers import designs

app = FastAPI(title="CADMIN - Lattice Design Suite")
app.include_router(designs.router)


@app.get("/health")
def health():
    return {"status": "ok"}