"""
FastAPI application for lead enrichment microservice.
"""
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}
