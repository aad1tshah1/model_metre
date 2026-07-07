from dataclasses import replace

from modelmetre.core.models import PromptRequest


class ConfigService:
    def get_default_provider(self) -> str:
        return "anthropic"

    def get_default_model(self) -> str:
        return "sonnet"

    def apply_defaults(self, request: PromptRequest) -> PromptRequest:
        return replace(
            request,
            provider=request.provider or self.get_default_provider(),
            model=request.model or self.get_default_model(),
        )