from typer.testing import CliRunner

from commerce_router import cli
from commerce_router.schema import Intent, ShopperRequest

runner = CliRunner()


def test_ask_prints_one_block_per_model(monkeypatch):
    def fake_extract(question, model):
        return ShopperRequest(intents=[Intent.ORDER_STATUS], order_id="48213", confidence=0.9), 12.3

    monkeypatch.setattr(cli, "extract", fake_extract)
    result = runner.invoke(cli.app, ["Where is my order 48213?", "--models", "small,large"])

    assert result.exit_code == 0
    assert "small (13 ms)" in result.output
    assert "large (12 ms)" in result.output
    assert '"order_id": "48213"' in result.output
