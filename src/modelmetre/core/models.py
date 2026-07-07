from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

@dataclass
class PromptRequest:
    prompt: str
    model: str | None = None
    provider: str | None = None
    temperature: float | None = None


@dataclass
class InteractionRecord:
    provider: str
    model: str
    prompt: str
    response: str
    input_tokens: int
    output_tokens: int
    latency_ms: int
    estimated_cost: Decimal
    estimated_energy: Decimal
    created_at: datetime