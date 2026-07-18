"""
Generate a company brochure by scraping a website and its relevant
sub-pages, then writing it up with Groq's free-tier hosted model.
"""

from groq import Groq

from src.config.settings import settings
from src.services.scraper import scrape_article, fetch_links
from src.services.link_selector import select_relevant_links

GROQ_MODEL = "llama-3.3-70b-versatile"

BROCHURE_SYSTEM_PROMPT = """
You are an assistant that creates a short, professional company brochure
in markdown for prospective customers, investors, and recruits.
Include company mission, culture, products, and careers info if available.
Respond in markdown, no code blocks.
"""


def call_llm(prompt: str, system: str) -> str:
    """
    Call Groq's free-tier hosted model (llama-3.3-70b-versatile).
    """
    client = Groq(api_key=settings.groq_api_key)
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()


def gather_company_content(company_name: str, url: str) -> str:
    """
    Scrape the landing page plus any relevant sub-pages (About, Careers, etc),
    combined into one text blob to feed to the brochure-writing LLM call.
    """
    content = f"## Landing page ({url})\n\n"
    content += scrape_article(url)[:3000]

    raw_links = fetch_links(url)
    relevant_links = select_relevant_links(url, raw_links)

    for link in relevant_links:
        try:
            page_text = scrape_article(link["url"])[:2000]
            content += f"\n\n## {link['type'].title()} ({link['url']})\n\n{page_text}"
        except Exception as exc:
            print(f"Skipped {link['url']}: {exc}")

    return content[:8000]


def create_brochure(company_name: str, url: str) -> str:
    """
    Full pipeline: scrape -> select relevant links -> gather content -> write brochure.
    """
    content = gather_company_content(company_name, url)
    prompt = f"Company: {company_name}\n\n{content}"
    return call_llm(prompt, BROCHURE_SYSTEM_PROMPT)


def stream_brochure(company_name: str, url: str):
    """
    Same as create_brochure, but yields text chunks as they arrive from Groq,
    for a live typewriter-style display in a notebook.
    """
    content = gather_company_content(company_name, url)
    prompt = f"Company: {company_name}\n\n{content}"

    client = Groq(api_key=settings.groq_api_key)
    stream = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": BROCHURE_SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        stream=True,
    )

    response = ""
    for chunk in stream:
        delta = chunk.choices[0].delta.content or ""
        response += delta
        yield response