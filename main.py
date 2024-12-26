import requests
from bs4 import BeautifulSoup
import calendar

def fetch_threads(url, keyword):
    print(f"Przeszukiwanie {url} pod kątem słowa kluczowego: {keyword}")
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Błąd podczas pobierania strony: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    threads = []

    for link in soup.find_all('a'):
        title = link.text.strip()
        href = link.get('href')
        if href and keyword.lower() in title.lower():
            threads.append({
                'title': title,
                'url': url.rsplit('/', 1)[0] + '/' + href
            })

    return threads

def search_archive(base_url, keyword, year_range):
    results = []
    for year in year_range:
        for month in range(1, 13):
            month_name = calendar.month_name[month]
            archive_url = f"{base_url}{year}-{month_name}/subject.html"
            try:
                threads = fetch_threads(archive_url, keyword)
                results.extend(threads)
            except Exception as e:
                print(f"Błąd przetwarzania {archive_url}: {e}")
    return results

BASE_URL = "https://lists.osgeo.org/pipermail/qgis-developer/"
KEYWORD = "Merge"
YEAR_RANGE = range(2023, 2025)

found_threads = search_archive(BASE_URL, KEYWORD, YEAR_RANGE)

print("\nZnalezione wątki:")
for thread in found_threads:
    print(f"- {thread['title']}: {thread['url']}")
