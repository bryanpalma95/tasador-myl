# Tasador Mitos y Leyendas

Tasador de precios de cartas Mitos y Leyendas desde una foto.

**Demo:** https://bryanpalma95.github.io/tasador-myl

## Arquitectura

| Capa | Tecnologia | Deploy |
|------|-----------|--------|
| Frontend | HTML + CSS + JS puro | GitHub Pages |
| Backend  | Python + FastAPI + EasyOCR | Render.com |

## Flujo

1. Sube la foto.
2. OCR detecta el nombre.
3. Confirmas o corriges el nombre.
4. Se busca en Gorila TCG, Cachorro Store y CameloTCG.
5. Tabla de resultados con minimo, promedio, mediana y maximo.

## Deploy

Ver DEPLOY.md para instrucciones paso a paso.