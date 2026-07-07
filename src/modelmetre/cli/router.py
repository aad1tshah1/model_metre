from modelmetre.cli.commands.prompt import handle_prompt
from modelmetre.cli.commands.stats import show_stats
from modelmetre.cli.parser import parse_prompt_args


def route(args: list[str]) -> None:
    if args[0] == "stats":
        show_stats()
        return

    request = parse_prompt_args(args)
    handle_prompt(request)