from abc import ABC, abstractmethod
from dataclasses import dataclass

from modelmetre.core.models import PromptRequest


@dataclass
class ProviderResponse:
    provider: str
    model: str
    text: str
    input_tokens: int
    output_tokens: int
    latency_ms: int


class Provider(ABC):
    @abstractmethod
    def send_prompt(self, request: PromptRequest) -> ProviderResponse:
        raise NotImplementedError