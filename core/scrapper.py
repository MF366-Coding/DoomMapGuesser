import requests


def scrape_json_contents(url: str):
    json_response = requests.get(url=url, timeout=2, allow_redirects=False)
    return json_response.json()


def scrape_byte_contents(url: str) -> bytes:
    json_response = requests.get(url=url, timeout=2, allow_redirects=False)
    return json_response.content


def scrape_string_contents(url: str) -> str:
    json_response = requests.get(url=url, timeout=2, allow_redirects=False)
    return json_response.text
