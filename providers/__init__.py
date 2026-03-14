"""
StratIQ Provider Interface
All providers implement: scan(url, api_key) and generate(context, api_key)
Both return dicts that map directly to the frontend data model.
"""

from .anthropic_provider import AnthropicProvider
from .openai_provider import OpenAIProvider
from .google_provider import GoogleProvider
from .openrouter_provider import OpenRouterProvider

PROVIDERS = {
    'anthropic': AnthropicProvider,
    'openai': OpenAIProvider,
    'google': GoogleProvider,
    'openrouter': OpenRouterProvider,
}

def get_provider(name: str):
    cls = PROVIDERS.get(name.lower())
    if not cls:
        raise ValueError(f"Unknown provider: {name}. Must be one of: {list(PROVIDERS.keys())}")
    return cls()
