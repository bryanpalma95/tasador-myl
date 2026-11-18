# Guia de Deploy

## 1. Backend en Render

1. Entra a dashboard.render.com
2. Click en New > Web Service
3. Conecta el repo bryanpalma95/tasador-myl
4. Configuracion:
   - Root Directory: backend
   - Build Command: pip install -r requirements.txt
   - Start Command: uvicorn app.main:app
   - Environment: Python 3
5. Click Create Web Service
6. Copia la URL que te da Render

## 2. Actualizar la URL en el frontend

En frontend/index.html busca:

  const API_URL = ...

Reemplaza por la URL que te dio Render.

## 3. Frontend en GitHub Pages

1. En GitHub, ve a Settings > Pages
2. Source: Deploy from a branch
3. Branch: main, Folder: /frontend
4. Click Save
5. En ~2 minutos la app estara en https://bryanpalma95.github.io/tasador-myl
