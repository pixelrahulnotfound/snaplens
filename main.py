from search import search_duckduckgo
from screenshot import screenshot_fullpage_base64

from concurrent.futures import ThreadPoolExecutor, as_completed
import webbrowser


def capture_all_screenshots(results, max_workers=5):
    screenshots = [None] * len(results)

    print("\nCapturing screenshots\n")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_index = {
            executor.submit(screenshot_fullpage_base64, r["url"]): idx
            for idx, r in enumerate(results)
        }

        for future in as_completed(future_to_index):
            idx = future_to_index[future]
            url = results[idx]["url"]
            try:
                screenshots[idx] = future.result()
                print(f"Screenshot captured for: {url}")
            except Exception as e:
                print(f"Screenshot failed for {url}: {e}")
                screenshots[idx] = None

    return screenshots


def build_html(results, screenshots, output="output.html"):
    html = "<html><body><h1>Visual Research Results</h1>"

    for item, b64 in zip(results, screenshots):
        html += f"<h2>{item['title']}</h2>"
        html += f"<p><a href='{item['url']}'>{item['url']}</a></p>"

        if b64:
            html += f"<img src='data:image/png;base64,{b64}' width='600'><br><br>"
        else:
            html += "<p><b>Screenshot failed.</b></p>"

    html += "</body></html>"

    with open(output, "w", encoding="utf-8") as f:
        f.write(html)

    return output 


def main():
    query = input("Enter your topic: ").strip()
    print(f"Searching for: {query}\n")

    limit = int(input("Enter how many sites you want to see: "))

    results = search_duckduckgo(query, limit)
    print(f"\nFound {len(results)} results.")

    screenshots = capture_all_screenshots(results)

    output_file = build_html(results, screenshots)

    
    webbrowser.open(output_file)   # <-- Auto-open HTML page


if __name__ == "__main__":
    main()
