"""
main.py — Backend Tasador MyL (solo scrapers, OCR en el navegador)
"""
from __future__ import annotations
import statistics
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.scrapers import buscar_todas

app = FastAPI(title="Tasador MyL API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

class BuscarRequest(BaseModel):
    nombre: str

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/buscar")
async def buscar(body: BuscarRequest):
    nombre = body.nombre.strip()
    if not nombre:
        return JSONResponse(status_code=400, content={"error": "nombre vacio"})
    resultados_obj = await buscar_todas(nombre)
    resultados = [
        {"tienda": r.tienda, "nombre": r.nombre, "precio": r.precio, "stock": r.stock, "url": r.url}
        for r in resultados_obj
    ]
    precios = [r["precio"] for r in resultados if r["precio"] and r["precio"] > 0]
    stats = {}
    if precios:
        stats = {
            "minimo": min(precios),
            "maximo": max(precios),
            "promedio": round(statistics.mean(precios)),
            "mediana": round(statistics.median(precios)),
            "total": len(resultados),
            "con_precio": len(precios),
        }
    return {"nombre_buscado": nombre, "resultados": resultados, "stats": stats}
