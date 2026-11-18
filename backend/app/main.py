"""
main.py — Backend Tasador MyL
Expone dos endpoints JSON consumidos por el frontend estático.
"""
from __future__ import annotations

import base64, io, statistics
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.ocr import extraer_nombre
from app.scrapers import buscar_todas

app = FastAPI(title="Tasador MyL API")

# CORS: permite que el frontend en GitHub Pages llame al backend en Render
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # en produccion reemplazar por la URL exacta de GitHub Pages
    allow_methods=["POST"],
    allow_headers=["*"],
)


class BuscarRequest(BaseModel):
    nombre: str


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/detectar")
async def detectar(foto: UploadFile = File(...)):
    """Recibe la foto y retorna el nombre detectado por OCR."""
    imagen_bytes = await foto.read()
    nombre = extraer_nombre(imagen_bytes)
    return {"nombre": nombre}


@app.post("/buscar")
async def buscar(body: BuscarRequest):
    """Busca el nombre en las tiendas y retorna la lista de resultados con estadísticas."""
    nombre = body.nombre.strip()
    if not nombre:
        return JSONResponse(status_code=400, content={"error": "nombre vacio"})

    resultados_obj = await buscar_todas(nombre)
    resultados = [
        {
            "tienda": r.tienda,
            "nombre": r.nombre,
            "precio": r.precio,
            "stock": r.stock,
            "url": r.url,
        }
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
