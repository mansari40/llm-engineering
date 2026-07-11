
# Day 1

On Day 1, I built a simple workflow that turned a Chinese-language news article from BBC website into English text and a short summary. The goal was to scrape the article content from the web, translate it into English and then summarize the main points.

I used `requests`, `BeautifulSoup`, `trafilatura` and `Selenium` libraries to extract article text from a webpage. For translation and summarization, I used Groq with the model ***llama-3.3-70b-versatile***, and I also set up a fallback to OpenAI ***gpt-4o-mini*** model if Groq was unavailable.

At first, the scraper ran into access issues because some websites block basic requests or reset connections. To solve that, I improved the request setup and added a browser-based fallback so the notebook could still retrieve the article content reliably.

