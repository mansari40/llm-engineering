"""
Downloading and extracting article content from webpages.
"""

from bs4 import BeautifulSoup
import requests
import trafilatura
from requests import RequestException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape_article(url: str) -> str:
    """
    Download a webpage and extract its readable text.

    Args:
        url: URL of the article.

    Returns:
        Clean article text.
    """

    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/137.0.0.0 Safari/537.36"
        )
    }

    response = None
    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=30,
        )
        response.raise_for_status()
    except RequestException as exc:
        response_error = exc
    else:
        response_error = None

    page_source = None
    for attempt in range(2):
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")

            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=chrome_options,
            )
            driver.get(url)
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "article"))
            )
            page_source = driver.page_source
            driver.quit()
            break
        except Exception:
            page_source = None
            continue

    if page_source:
        downloaded = trafilatura.extract(
            page_source,
            include_links=False,
            include_images=False,
            output_format="txt",
            url=url,
        )
        if downloaded:
            return downloaded

        soup = BeautifulSoup(page_source, "lxml")
        paragraphs = soup.find_all("p")
        article = "\n".join(
            paragraph.get_text(strip=True)
            for paragraph in paragraphs
        )
        if article:
            return article

    if response is not None:
        downloaded = trafilatura.extract(
            response.text,
            include_links=False,
            include_images=False,
            output_format="txt",
            url=url,
        )
        if downloaded:
            return downloaded

        soup = BeautifulSoup(response.text, "lxml")
        paragraphs = soup.find_all("p")
        article = "\n".join(
            paragraph.get_text(strip=True)
            for paragraph in paragraphs
        )
        if article:
            return article

    raise RuntimeError(f"Failed to fetch article: {response_error}")