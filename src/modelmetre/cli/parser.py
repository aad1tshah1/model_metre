from modelmetre.core.models import PromptRequest


def parse_prompt_args(args: list[str]) -> PromptRequest:
    model = None
    provider = None
    temperature = None
    prompt_words = []

    index = 0

    while index < len(args):
        current = args[index]

        if current == "--model":
            model = args[index + 1]
            index += 2
        elif current == "--provider":
            provider = args[index + 1]
            index += 2
        elif current == "--temperature":
            temperature = float(args[index + 1])
            index += 2
        else:
            prompt_words.append(current)
            index += 1

    prompt = " ".join(prompt_words)

    return PromptRequest(
        prompt=prompt,
        model=model,
        provider=provider,
        temperature=temperature,
    )