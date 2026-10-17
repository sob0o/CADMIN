from fastapi import FastAPI

app = FastAPI(title="CADMIN - Lattice Design Suite")


@app.get("/health")
def health():
    return {"status": "ok"}