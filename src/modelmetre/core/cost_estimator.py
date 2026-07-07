from decimal import Decimal


ANTHROPIC_PRICING_USD_PER_MILLION = {
    "claude-haiku-4-5": {
        "input": Decimal("1.00"),
        "output": Decimal("5.00"),
    },
    "claude-sonnet-4-5": {
        "input": Decimal("3.00"),
        "output": Decimal("15.00"),
    },
    "claude-opus-4-1": {
        "input": Decimal("15.00"),
        "output": Decimal("75.00"),
    },
}


def normalize_anthropic_model(model: str) -> str:
    if model.startswith("claude-haiku-4-5"):
        return "claude-haiku-4-5"

    if model.startswith("claude-sonnet-4-5"):
        return "claude-sonnet-4-5"

    if model.startswith("claude-opus-4-1"):
        return "claude-opus-4-1"

    return model


class CostEstimator:
    def estimate(
        self,
        provider: str,
        model: str,
        input_tokens: int,
        output_tokens: int,
    ) -> Decimal:
        if provider != "anthropic":
            return Decimal("0.00")

        normalized_model = normalize_anthropic_model(model)

        pricing = ANTHROPIC_PRICING_USD_PER_MILLION.get(normalized_model)

        if pricing is None:
            return Decimal("0.00")

        input_cost = (
            Decimal(input_tokens) / Decimal("1000000")
        ) * pricing["input"]

        output_cost = (
            Decimal(output_tokens) / Decimal("1000000")
        ) * pricing["output"]

        return input_cost + output_cost