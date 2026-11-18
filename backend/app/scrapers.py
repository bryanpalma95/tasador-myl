"""
scrapers.py — busqueda de precios en tiendas MyL
Tiendas: Gorila TCG, Cachorro Store, CameloTCG
URLs verificadas: noviembre 2026
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
    nums = re.findall(r"\d+", texto.replace(".", "").replace(",", ""))
    return int(nums[0]) if nums else None


async def buscar_gorila(nombre: str, client: httpx.AsyncClient) -> list[Resultado]:
    """Gorila TCG — www.gorilatcg.cl"""
    resultados = []
    try:
        url = f"https://www.gorilatcg.cl/search?q={nombre.replace(' ', '+')}"
        r = await client.get(url, headers=HEADERS, timeout=12)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        # Buscar productos en diferentes estructuras posibles
        productos = (
            soup.select(".product-item, .prod-container, [class*='product']")
            or soup.select("article")
        )[:5]
        for p in productos:
            titulo_el = p.select_one("h2, h3, .product-name, [class*='title'], [class*='name']")
            precio_el = p.select_one("[class*='price'], .precio, .amount")
            link_el   = p.select_one("a[href]")
            titulo = titulo_el.get_text(strip=True) if titulo_el else "?"
            precio_txt = precio_el.get_text(strip=True) if precio_el else ""
            href = link_el["href"] if link_el else url
            if href.startswith("/"):
                href = "https://www.gorilatcg.cl" + href
            resultados.append(Resultado(
                tienda="Gorila TCG", nombre=titulo,
                precio=_limpiar_precio(precio_txt), stock=None, url=href,
            ))
        if not resultados:
            resultados.append(Resultado(tienda="Gorila TCG", nombre="Sin resultados", precio=None, stock=None, url=url))
    except Exception as e:
        resultados.append(Resultado(tienda="Gorila TCG", nombre=f"Error: {e}", precio=None, stock=None, url=""))
    return resultados


async def buscar_cachorro(nombre: str, client: httpx.AsyncClient) -> list[Resultado]:
    """Cachorro Store — cachorrostore.cl (WooCommerce)"""
    resultados = []
    try:
        url = f"https://cachorrostore.cl/?s={nombre.replace(' ', '+')}&post_type=product"
        r = await client.get(url, headers=HEADERS, timeout=12)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        productos = soup.select("li.product, .product-item, .type-product")[:5]
        for p in productos:
            titulo_el = p.select_one("h2.woocommerce-loop-product__title, h2, h3, .product-title")
            precio_el = p.select_one(".price ins .amount, .price .amount, .price, bdi")
            link_el   = p.select_one("a.woocommerce-loop-product__link, a[href]")
            titulo = titulo_el.get_text(strip=True) if titulo_el else "?"
            precio_txt = precio_el.get_text(strip=True) if precio_el else ""
            href = link_el["href"] if link_el else url
            stock_el = p.select_one(".stock, .out-of-stock")
            stock = stock_el.get_text(strip=True) if stock_el else None
            resultados.append(Resultado(
                tienda="Cachorro Store", nombre=titulo,
                precio=_limpiar_precio(precio_txt), stock=stock, url=href,
            ))
        if not resultados:
            resultados.append(Resultado(tienda="Cachorro Store", nombre="Sin resultados", precio=None, stock=None, url=url))
    except Exception as e:
        resultados.append(Resultado(tienda="Cachorro Store", nombre=f"Error: {e}", precio=None, stock=None, url=""))
    return resultados


async def buscar_camelo(nombre: str, client: httpx.AsyncClient) -> list[Resultado]:
    """CameloTCG — camelotcg.cl (WooCommerce)"""
    resultados = []
    try:
        url = f"https://camelotcg.cl/?s={nombre.replace(' ', '+')}&post_type=product"
        r = await client.get(url, headers=HEADERS, timeout=12)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        productos = soup.select("li.product, .product-item, .type-product")[:5]
        for p in productos:
            titulo_el = p.select_one("h2.woocommerce-loop-product__title, h2, h3, .product-title")
            precio_el = p.select_one(".price ins .amount, .price .amount, .price, bdi")
            link_el   = p.select_one("a.woocommerce-loop-product__link, a[href]")
            titulo = titulo_el.get_text(strip=True) if titulo_el else "?"
            precio_txt = precio_el.get_text(strip=True) if precio_el else ""
            href = link_el["href"] if link_el else url
            if href.startswith("/"):
                href = "https://camelotcg.cl" + href
            resultados.append(Resultado(
                tienda="CameloTCG", nombre=titulo,
                precio=_limpiar_precio(precio_txt), stock=None, url=href,
            ))
        if not resultados:
            resultados.append(Resultado(tienda="CameloTCG", nombre="Sin resultados", precio=None, stock=None, url=url))
    except Exception as e:
        resultados.append(Resultado(tienda="CameloTCG", nombre=f"Error: {e}", precio=None, stock=None, url=""))
    return resultados


async def buscar_todas(nombre: str) -> list[Resultado]:
    async with httpx.AsyncClient(follow_redirects=True) as client:
        resultados = await asyncio.gather(
            buscar_gorila(nombre, client),
            buscar_cachorro(nombre, client),
            buscar_camelo(nombre, client),
        )
    return [r for lista in resultados for r in lista]
