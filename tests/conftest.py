from datetime import datetime
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from modelmetre.core.models import InteractionRecord


@pytest.fixture
def make_record():
    def _make_record(
        estimated_cost: float = 1.25,
        input_tokens: int = 10,
        output_tokens: int = 5,
    ) -> InteractionRecord:
        return InteractionRecord(
            provider="anthropic",
            model="sonnet",
            prompt="Explain BFS",
            response="A response",
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            latency_ms=120,
            estimated_cost=estimated_cost,
            estimated_energy=0.5,
            created_at=datetime(2024, 1, 1, 12, 0, 0),
        )

    return _make_record