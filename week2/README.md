# Day 1

I set up a unified way to talk to multiple LLM providers, using the fact that Gemini, Groq, and OpenRouter all expose OpenAI-compatible endpoints, so I could reuse the same OpenAI client and just swap the base_url and API key for each one. I also connected to a local `gpt-oss:20b` model running through Ollama the same way, and wrapped it in LangChain's ChatOpenAI to compare against calling it directly.

I compared the same prompt across OpenAI, Gemini, OpenRouter's `z-ai/glm-4.6v`, and the local Ollama model, the local model was noticeably slower on some tasks. I also tested the reasoning_effort argument and saw a real accuracy improvement switching it from minimal to low.

As a fun exercise, I built a three-way debate: Gemini, OpenRouter, and Ollama each played a persona (optimist, pessimist, mediator) arguing about VAR at the 2026 World Cup, with real details about the tournament's new officiating tech baked into each persona's prompt.

# Day 2

I compared zero-shot vs few-shot prompting on a single task, using Groq's free-tier `llama-3.3-70b-versatile` model as the constant. I created a small fictional company, CloudNova IT Solutions, that only sells Azure cloud and software services, with a 20% discount overall and 40% on Azure, giving the assistant clear rules to follow. I wrote two system prompts for the same sales-chatbot task: a zero-shot version with just the instruction and facts, and a few-shot version with a few example conversations showing how to redirect AWS/hardware questions to Azure and consistently push the 40% discount. Both ran through Gradio's `ChatInterface`, which handed me the full conversation history each turn for multi-turn memory with no extra code.

I hit a couple of snags along the way - a Gradio version mismatch around the `type="messages"` argument, and a 400 error from Groq caused by an extra `metadata` field in Gradio's history dicts - both fixed by cleaning the history down to just `role` and `content`. Once running, the difference was clear: zero-shot occasionally drifted off the "no AWS, no hardware" rules or forgot the Azure discount, while few-shot stayed on-message every time.

# Day 3

I built a hotel booking agent using tool calling backed by a real SQLite database, instead of letting the model guess at hotel names or prices. I set up a `hotels.db` with a `hotels` table (name, city, category, price, rating, amenities) seeded across budget/reasonable/luxurious tiers in a few cities, plus a `bookings` table to record reservations.

I defined four tools - `search_hotels`, `get_hotel_details`, `compare_hotels`, and `book_hotel` - and wrote a loop that lets the model call one or more of them per turn, feeds the results back, and repeats until it has a real answer, so a single message like "compare the reasonable hotels in Rome and Paris" can trigger multiple tool calls before the customer sees a reply. Same as Day 2, I used Gradio's `ChatInterface` for history/memory, and reused the fix for stripping history down to `role`/`content` before sending it to Groq.

# Day 4

I extended the tool-calling pattern from Day 3 into a multi-provider assistant, using the same OpenAI-compatible-endpoint trick from Day 1 to let a customer pick between Groq, Gemini, and OpenRouter for the same conversation. The tool-calling loop itself stayed generic - it now takes `client` and `model` as arguments instead of being hardcoded to one provider, so the same function works no matter which one is selected from a dropdown. I also added free text-to-speech with `gTTS` so replies get spoken aloud, and switched from `gr.ChatInterface` to `gr.Blocks` to fit the provider dropdown and audio player alongside the chat.

For the hotel data, I swapped the local SQLite database for Makcorps, a real third-party hotel price API. Getting there took some debugging - a deprecated endpoint, then a city-search endpoint gated behind a paid plan - before I landed on what the free tier actually supports: looking up a hotel by name via the Mapping API, then pulling live prices for that hotel ID. Adjusted the tool description and system prompt so the assistant asks for a hotel name instead of just a city.


