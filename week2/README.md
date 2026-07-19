# Day 1 (Week 2)

I set up a unified way to talk to multiple LLM providers, using the fact that Gemini, Groq, and OpenRouter all expose OpenAI-compatible endpoints, so I could reuse the same OpenAI client and just swap the base_url and API key for each one. I also connected to a local `gpt-oss:20b` model running through Ollama the same way, and wrapped it in LangChain's ChatOpenAI to compare against calling it directly.

I compared the same prompt across OpenAI, Gemini, OpenRouter's `z-ai/glm-4.6v`, and the local Ollama model, the local model was noticeably slower on some tasks. I also tested the reasoning_effort argument and saw a real accuracy improvement switching it from minimal to low.

As a fun exercise, I built a three-way debate: Gemini, OpenRouter, and Ollama each played a persona (optimist, pessimist, mediator) arguing about VAR at the 2026 World Cup, with real details about the tournament's new officiating tech baked into each persona's prompt.