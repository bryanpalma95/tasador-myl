"""
ocr.py — extrae el nombre de la carta desde una imagen usando EasyOCR.
Estrategia simple: toma las primeras lineas del texto detectado que
probablemente corresponden al titulo de la carta.
"""
from __future__ import annotations
import io, re
from pathlib import Path
from PIL import Image

_reader = None  # inicializado en la primera llamada (carga el modelo una vez)


def _get_reader():
    global _reader
    if _reader is None:
        import easyocr
        _reader = easyocr.Reader(["es", "en"], gpu=False, verbose=False)
    return _reader


def _limpiar(texto: str) -> str:
    """Elimina caracteres raros y normaliza espacios."""
    texto = re.sub(r"[^\w\s\-\'\u00C0-\u024F]", " ", texto)
    return re.sub(r"\s+", " ", texto).strip()


def extraer_nombre(imagen_bytes: bytes) -> str:
    """
    Recibe los bytes de la imagen y retorna el nombre probable de la carta.
    Estrategia: las primeras 1-2 lineas de texto detectado suelen ser el titulo.
    """
    img = Image.open(io.BytesIO(imagen_bytes)).convert("RGB")
    reader = _get_reader()
    resultados = reader.readtext(img, detail=1, paragraph=False)

    if not resultados:
        return ""

    # Ordenar por posicion vertical (top-y de la bounding box)
    resultados_ord = sorted(resultados, key=lambda r: r[0][0][1])

    # Tomar las primeras 2 detecciones con confianza >= 0.4
    candidatos = [
        texto for _, texto, conf in resultados_ord if conf >= 0.4
    ][:2]

    nombre = " ".join(_limpiar(c) for c in candidatos if c)
    return nombre.strip()
