"""
scrapers.py — busqueda de precios en tiendas MyL
Tiendas: Gorila TCG, Cachorro Store, CameloTCG
"""
import httpx
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import Optional
import asyncio, re

@dataclass
class Resultado:
    tienda: str
    nombre: str
    precio: Optional[int]
    stock: Optional[str]
    url: str

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

def _limpiar_precio(texto: str) -> Optional[int]:
    """Extrae el primer numero entero de un string con precio."""
    nums = re.findall(r"\d+", texto.replace(".", "").replace(",", ""))
    return int(nums[0]) if nums else None


async def buscar_gorila(nombre: str, client: httpx.AsyncClient) -> list[Resultado]:
    """Gorila TCG — tienda.gorilatcg.cl"""
    resultados = []
    try:
        url = f"https://tienda.gorilatcg.cl/search?q={httpx.QueryParams({'q': nombre})}"
        # construir query correctamente
        url = f"https://tienda.gorilatcg.cl/search?q={nombre.replace(' ', '+')}&type=product"
        r = await client.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        productos = soup.select(".grid-product__content")[:5]
        for p in productos:
            titulo_el = p.select_one(".grid-product__title")
            precio_el = p.select_one(".grid-product__price")
            link_el = p.select_one("a")
            titulo = titulo_el.get_text(strip=True) if titulo_el else "?"
            precio_txt = precio_el.get_text(strip=True) if precio_el else ""
            href = "https://tienda.gorilatcg.cl" + link_el["href"] if link_el else url
            resultados.append(Resultado(
                tienda="Gorila TCG",
                nombre=titulo,
                precio=_limpiar_precio(precio_txt),
                stock=None,
                url=href,
            ))
    except Exception as e:
        resultados.append(Resultado(tienda="Gorila TCG", nombre=f"Error: {e}", precio=None, stock=None, url=""))
    return resultados


async def buscar_cachorro(nombre: str, client: httpx.AsyncClient) -> list[Resultado]:
    """Cachorro Store — cachorro.cl"""
    resultados = []
    try:
        url = f"https://cachorro.cl/search?type=product&q={nombre.replace(' ', '+')}"
        r = await client.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        productos = soup.select(".product-item")[:5]
        for p in productos:
            titulo_el = p.select_one(".product-item__title") or p.select_one("h2")
            precio_el = p.select_one(".price__regular .price-item") or p.select_one(".price")
            link_el = p.select_one("a")
            titulo = titulo_el.get_text(strip=True) if titulo_el else "?"
            precio_txt = precio_el.get_text(strip=True) if precio_el else ""
            href = "https://cachorro.cl" + link_el["href"] if link_el and link_el.get("href","").startswith("/") else (link_el["href"] if link_el else url)
            resultados.append(Resultado(
                tienda="Cachorro Store",
                nombre=titulo,
                precio=_limpiar_precio(precio_txt),
                stock=None,
                url=href,
            ))
    except Exception as e:
        resultados.append(Resultado(tienda="Cachorro Store", nombre=f"Error: {e}", precio=None, stock=None, url=""))
    return resultados


async def buscar_camelo(nombre: str, client: httpx.AsyncClient) -> list[Resultado]:
    """CameloTCG — camelotcg.cl"""
    resultados = []
    try:
        url = f"https://www.camelotcg.cl/search?type=product&q={nombre.replace(' ', '+')}"
        r = await client.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        productos = soup.select(".product-item, .grid__item")[:5]
        for p in productos:
            titulo_el = p.select_one(".product-item__title, .product-title, h2, h3")
            precio_el = p.select_one(".price-item, .price, .product-price")
            link_el = p.select_one("a")
            titulo = titulo_el.get_text(strip=True) if titulo_el else "?"
            precio_txt = precio_el.get_text(strip=True) if precio_el else ""
            href = link_el["href"] if link_el else url
            if href.startswith("/"):
                href = "https://www.camelotcg.cl" + href
            resultados.append(Resultado(
                tienda="CameloTCG",
                nombre=titulo,
                precio=_limpiar_precio(precio_txt),
                stock=None,
                url=href,
            ))
    except Exception as e:
        resultados.append(Resultado(tienda="CameloTCG", nombre=f"Error: {e}", precio=None, stock=None, url=""))
    return resultados


async def buscar_todas(nombre: str) -> list[Resultado]:
    """Busca en paralelo en las tres tiendas."""
    async with httpx.AsyncClient(follow_redirects=True) as client:
        resultados = await asyncio.gather(
            buscar_gorila(nombre, client),
            buscar_cachorro(nombre, client),
            buscar_camelo(nombre, client),
        )
    todos = [r for lista in resultados for r in lista]
    return todos
