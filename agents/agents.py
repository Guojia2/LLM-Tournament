import os
from dotenv import load_dotenv

load_dotenv()

"""
I'm currently using my own API keys on the free tier for Anthropic and Google.
OpenAI has no free tier, so it is not being used for now, as of November 8, 2025.
Will have to contact project lead for their API keys, probably. I definitely don't
want to pay for several hundred runs of this, haha.

- Guojia La

"""
class Agent:
    def __init__(self, name, model="claude", model_config=None):
        self.name = name
        self.model = model
        self.model_config = model_config or {}
        self.client = None
        self.provider = None

        self._setup_client()

    def _setup_client(self):
        # OpenAI requires paid credits - skip for now
        # if self.model.startswith("gpt") or self.model.startswith("o1"):
        #     from openai import OpenAI
        #     self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        #     self.provider = "openai"

        if self.model.startswith("claude"):
            from anthropic import Anthropic
            self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            self.provider = "anthropic"

        elif self.model.startswith("gemini"):
            import google.generativeai as genai
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
            self.client = genai.GenerativeModel(self.model)
            self.provider = "gemini"

        else:
            self.provider = "dummy"

    def act(self, observation):
        if self.provider == "openai":
            return self._call_openai(observation)
        elif self.provider == "anthropic":
            return self._call_anthropic(observation)
        elif self.provider == "gemini":
            return self._call_gemini(observation)
        else:
            return "dummy_action"

    def _call_openai(self, observation):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": observation}],
                temperature=self.model_config.get("temperature", 0.7),
                max_tokens=self.model_config.get("max_tokens", 512),
                **{k: v for k, v in self.model_config.items()
                   if k not in ["temperature", "max_tokens"]}
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return f"ERROR: {str(e)}"

    def _call_anthropic(self, observation):
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.model_config.get("max_tokens", 1024),
                temperature=self.model_config.get("temperature", 0.7),
                messages=[{"role": "user", "content": observation}],
                **{k: v for k, v in self.model_config.items()
                   if k not in ["temperature", "max_tokens"]}
            )
            return response.content[0].text.strip()
        except Exception as e:
            print(f"Anthropic API error: {e}")
            return f"ERROR: {str(e)}"

    def _call_gemini(self, observation):
        try:
            response = self.client.generate_content(
                observation,
                generation_config={
                    "temperature": self.model_config.get("temperature", 0.7),
                    "max_output_tokens": self.model_config.get("max_tokens", 512),
                }
            )
            return response.text.strip()
        except Exception as e:
            print(f"Gemini API error: {e}")
            return f"ERROR: {str(e)}"