import typer

from modelmetre.storage.repository import UsageRepository, get_default_repository


def show_stats(repository: UsageRepository | None = None) -> None:
    repo = repository or get_default_repository()
    summary = repo.get_summary()

    typer.echo("ModelMeter usage summary")
    typer.echo(f"Total interactions: {summary['total_interactions']}")
    typer.echo(f"Total cost: ${summary['total_cost']:.4f}")
    typer.echo(f"Total tokens: {summary['total_tokens']}")