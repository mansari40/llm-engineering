# Day 1 (Week 2)

I set up a unified way to talk to multiple LLM providers, using the fact that Gemini, Groq, and OpenRouter all expose OpenAI-compatible endpoints, so I could reuse the same OpenAI client and just swap the base_url and API key for each one. I also connected to a local `gpt-oss:20b` model running through Ollama the same way, and wrapped it in LangChain's ChatOpenAI to compare against calling it directly.

I compared the same prompt across OpenAI, Gemini, OpenRouter's `z-ai/glm-4.6v`, and the local Ollama model, the local model was noticeably slower on some tasks. I also tested the reasoning_effort argument and saw a real accuracy improvement switching it from minimal to low.

As a fun exercise, I built a three-way debate: Gemini, OpenRouter, and Ollama each played a persona (optimist, pessimist, mediator) arguing about VAR at the 2026 World Cup, with real details about the tournament's new officiating tech baked into each persona's prompt.

# Day 2 (Week 2)

I compared zero-shot vs few-shot prompting on a single task, using Groq's free-tier `llama-3.3-70b-versatile` model as the constant. I created a small fictional company, CloudNova IT Solutions, that only sells Azure cloud and software services, with a 20% discount overall and 40% on Azure, giving the assistant clear rules to follow. I wrote two system prompts for the same sales-chatbot task: a zero-shot version with just the instruction and facts, and a few-shot version with a few example conversations showing how to redirect AWS/hardware questions to Azure and consistently push the 40% discount. Both ran through Gradio's `ChatInterface`, which handed me the full conversation history each turn for multi-turn memory with no extra code.

I hit a couple of snags along the way - a Gradio version mismatch around the `type="messages"` argument, and a 400 error from Groq caused by an extra `metadata` field in Gradio's history dicts - both fixed by cleaning the history down to just `role` and `content`. Once running, the difference was clear: zero-shot occasionally drifted off the "no AWS, no hardware" rules or forgot the Azure discount, while few-shot stayed on-message every time.