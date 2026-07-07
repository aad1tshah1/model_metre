from modelmetre.cli.commands.stats import show_stats
from modelmetre.storage.in_memory_repository import InMemoryUsageRepository


def test_show_stats_outputs_summary(capsys, make_record) -> None:
    repository = InMemoryUsageRepository()
    repository.save(make_record(estimated_cost=2.5, input_tokens=3, output_tokens=7))

    show_stats(repository=repository)

    captured = capsys.readouterr()
    assert "ModelMeter usage summary" in captured.out
    assert "Total interactions" in captured.out
    assert "2.5000" in captured.out