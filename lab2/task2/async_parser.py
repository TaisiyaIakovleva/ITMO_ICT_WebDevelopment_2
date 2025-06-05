# import asyncio
# import time
# from bs4 import BeautifulSoup
# from aiohttp import ClientSession, ClientTimeout, TCPConnector
# from db import init_db, save_parsed_page
# from urls import URLS

# CONNECTIONS_LIMIT = 20
# TIMEOUT = 10

# async def fetch(session, url):
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
#     }
#     try:
#         async with session.get(url, headers=headers, timeout=ClientTimeout(total=TIMEOUT)) as response:
#             html = await response.text()
#             soup = BeautifulSoup(html, "html.parser")
#             title = soup.title.string.strip() if soup.title else "No title"
#             return url, title
#     except Exception as e:
#         return url, f"[ERROR] {e}"

# async def parse_all(urls):
#     connector = TCPConnector(limit=CONNECTIONS_LIMIT)
#     async with ClientSession(connector=connector) as session:
#         tasks = [fetch(session, url) for url in urls]
#         results = await asyncio.gather(*tasks)
#         for url, title in results:
#             await save_parsed_page(url, title)

# async def main():
#     await init_db()
#     start = time.time()
#     await parse_all(URLS)
#     print("Asyncio done in", time.time() - start, "seconds")

# if __name__ == "__main__":
#     asyncio.run(main())
import aiohttp, asyncio, time
from bs4 import BeautifulSoup
from db import engine
from sqlmodel import Session
from models import ParsedPage
from urls import URLS
from aiohttp import ClientTimeout

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
}

async def fetch(session, url):
    try:
        async with session.get(url, headers=headers, timeout=ClientTimeout(total=10)) as response:
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")
            title = soup.title.string.strip() if soup.title else "No title"
            return url, title
    except Exception as e:
        return url, f"[ERROR] {e}"

async def parse_and_save(url):
    async with aiohttp.ClientSession() as session:
        url, title = await fetch(session, url)
        with Session(engine) as db:
            db.add(ParsedPage(url=url, title=title))
            db.commit()
        print(f"[{url}] -> {title}")

async def main():
    tasks = [parse_and_save(url) for url in URLS]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    print(f"Finished in {time.perf_counter() - start:.2f}s")
