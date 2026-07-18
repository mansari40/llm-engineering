"""
Use an LLM to decide which links on a company webpage are relevant
for building a brochure (About, Careers, Company, Product pages, etc).
"""

import json

from groq import Groq

from src.config.settings import settings

GROQ_MODEL = "llama-3.3-70b-versatile"

LINK_SYSTEM_PROMPT = """
You are given a list of links found on a company webpage.
Decide which links are relevant to include in a company brochure -
things like About, Company, Careers/Jobs, Team, or Product pages.
Ignore Terms of Service, Privacy Policy, login, and social media links.

Respond ONLY with JSON in this exact format:
{
    "links": [
        {"type": "about page", "url": "https://full.url/about"},
        {"type": "careers page", "url": "https://full.url/careers"}
    ]
}
"""


def select_relevant_links(url: str, raw_links: list[str]) -> list[dict]:
    """
    Given a base URL and a list of raw links found on it, ask the LLM
    to pick out the ones worth including in a brochure and resolve them
    to full URLs.

    Args:
        url: The base URL the links were found on.
        raw_links: Raw href values scraped from the page.

    Returns:
        List of dicts like {"type": "about page", "url": "https://..."}.
    """
    client = Groq(api_key=settings.groq_api_key)

    user_prompt = (
        f"Here are the links found on {url}. Some may be relative - "
        f"resolve them to full URLs based on the base site.\n\n"
        + "\n".join(raw_links)
    )

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": LINK_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.1,
    )

    result = json.loads(response.choices[0].message.content)
    return result.get("links", [])