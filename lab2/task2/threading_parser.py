# import threading
# import time
# from db import init_db, save_parsed_page
# from urls import URLS
# from common import get_title

# def parse_and_save(url):
#     title = get_title(url)
#     save_parsed_page(url, title)
#     print(f"[threading] {url} -> {title}")

# def main():
#     init_db()
#     threads = []

#     start = time.time()
#     for url in URLS:
#         t = threading.Thread(target=parse_and_save, args=(url,))
#         threads.append(t)
#         t.start()

#     for t in threads:
#         t.join()

#     print("Threading done in", time.time() - start, "seconds")

# if __name__ == "__main__":
#     main()
import threading, time, requests
from bs4 import BeautifulSoup
from models import ParsedPage
from db import engine
from sqlmodel import Session
from urls import URLS

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
}


def parse_and_save(url):
    try:
        html = requests.get(url, headers=headers, timeout=10).text
        soup = BeautifulSoup(html, "html.parser")
        title = soup.title.string.strip() if soup.title else "No title"
    except Exception as e:
        title = f"[ERROR] {e}"
    with Session(engine) as db:
        db.add(ParsedPage(url=url, title=title))
        db.commit()
    print(f"[{url}] -> {title}")

def main():
    threads = []
    for url in URLS:
        t = threading.Thread(target=parse_and_save, args=(url,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

if __name__ == "__main__":
    start = time.perf_counter()
    main()
    print(f"Finished in {time.perf_counter() - start:.2f}s")


