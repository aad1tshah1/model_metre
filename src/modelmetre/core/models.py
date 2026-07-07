from dataclasses import dataclass
from datetime import datetime


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
    estimated_cost: float
    estimated_energy: float
    created_at: datetime