import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/121.0.0.0 Safari/537.36"
    )
}

# limit = int(input("enter how many sites you want to see: "))

def search_duckduckgo(query: str, limit: int):
    url = "https://html.duckduckgo.com/html/"
    data = {"q": query}

    response = requests.post(url, headers=HEADERS, data=data)
    soup = BeautifulSoup(response.text, "html.parser")   

    results = []
    for a in soup.select(".result__a")[:limit]:
        title = a.text.strip()
        link = a.get("href")

        if link.startswith("/"):
            continue

        results.append({"title": title, "url": link})

    return results
