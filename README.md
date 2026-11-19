# Tasador Mitos y Leyendas

![Visitas](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fbryanpalma95.github.io%2Ftasador-myl&count_bg=%237C5CBF&title_bg=%23110E1E&icon=&icon_color=%23E7E7E7&title=visitas&edge_flat=true)

Tasador de precios de cartas Mitos y Leyendas desde una foto.

**Demo:** https://bryanpalma95.github.io/tasador-myl

## Arquitectura

| Capa | Tecnologia | Deploy |
|------|-----------|--------|
| Frontend | HTML + CSS + JS puro | GitHub Pages |
| Backend  | Python + FastAPI | Render.com |

## Flujo

1. Abre la camara o sube una foto de la carta.
2. Groq IA identifica el nombre automaticamente.
3. Se busca en Gorila TCG, Cachorro Store y CameloTCG.
4. Tabla de resultados con minimo, promedio, mediana y maximo.

## Deploy

Ver DEPLOY.md para instrucciones paso a paso.
