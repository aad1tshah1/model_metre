from modelmetre.cli.parser import parse_prompt_args


def test_parse_prompt_args_collects_flags_and_prompt() -> None:
    request = parse_prompt_args(
        ["--model", "opus", "--provider", "openai", "--temperature", "0.2", "Explain", "BFS"]
    )

    assert request.prompt == "Explain BFS"
    assert request.model == "opus"
    assert request.provider == "openai"
    assert request.temperature == 0.2


def test_parse_prompt_args_defaults_to_none_when_flags_missing() -> None:
    request = parse_prompt_args(["Explain", "BFS"])

    assert request.prompt == "Explain BFS"
    assert request.model is None
    assert request.provider is None
    assert request.temperature is None