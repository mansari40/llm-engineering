
# Day 1

On Day 1, I built a simple workflow that turned a Chinese-language news article from BBC website into English text and a short summary. The goal was to scrape the article content from the web, translate it into English and then summarize the main points.

I used `requests`, `BeautifulSoup`, `trafilatura` and `Selenium` libraries to extract article text from a webpage. For translation and summarization, I used Groq with the model ***llama-3.3-70b-versatile***, and I also set up a fallback to OpenAI ***gpt-4o-mini*** model if Groq was unavailable.

At first, the scraper ran into access issues because some websites block basic requests or reset connections. To solve that, I improved the request setup and added a browser-based fallback so the notebook could still retrieve the article content reliably.

# Day 2

On Day 2, I explored running open-source Large Language Models (LLMs) locally using **Ollama**. I downloaded and experimented with several models, including **Llama 3.2**, **DeepSeek-R1:1.5B**, and **Qwen3:8B**, and learned how to interact with them through both the Ollama command-line interface and its local REST API.

To evaluate their capabilities, I translated the same Chinese BBC news article using different models and compared their translation quality and response latency. The experiment highlighted clear differences in accuracy, completeness and execution speed. While the cloud-hosted **llama-3.3-70b-versatile** model delivered the highest-quality translation with the lowest response time, the locally executed models demonstrated the trade-off between model size, hardware limitations, and translation performance.

Additionally, I configured API keys using a `.env` file, connected to Ollama through `localhost:11434`, and gained a better understanding of the differences between cloud-hosted and locally deployed LLMs.

# Day 3
On Day 3, I built a company brochure generator, extending the scrape → LLM pipeline from Day 1 into a multi-step, multi-page workflow. Given a company name and its website, the tool scrapes the homepage, uses an LLM to decide which of the site's links are actually relevant (About, Careers, Product pages, etc.), scrapes those pages too, and combines everything into a short markdown brochure — useful for prospective customers, investors, or recruits.
I reused my existing `scrape_article` scraper and `Settings` class from Day 1, and added two new modules: `link_selector.py`, which asks Groq's **llama-3.3-70b-versatile** model to filter a page's raw links down to the relevant ones and return them as structured JSON, and `brochure.py`, which chains the scraping and link-selection steps together and writes the final brochure. This pipeline runs entirely on Groq's free-tier model rather than a paid OpenAI model, and inherits the more robust fallback scraping (Selenium → trafilatura → BeautifulSoup) built in Day 1.
I generated a brochure for **NVIDIA** as the test case, and also added a streaming variant so the brochure renders live, typewriter-style, in the notebook.


