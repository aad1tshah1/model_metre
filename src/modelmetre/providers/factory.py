import os

from modelmetre.providers.anthropic import AnthropicProvider
from modelmetre.providers.base import Provider
from modelmetre.providers.fake import FakeProvider


class ProviderFactory:
    def create(self, provider_name: str | None) -> Provider:
        if provider_name == "anthropic":
            api_key = os.environ.get("ANTHROPIC_API_KEY")

            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY is not set")

            return AnthropicProvider(api_key=api_key)

        return FakeProvider()