import typer

from modelmetre.core.models import PromptRequest
from modelmetre.core.prompt_service import PromptService


def handle_prompt(request: PromptRequest) -> None:
    service = PromptService()
    record = service.ask(request)

    typer.echo(record.response)