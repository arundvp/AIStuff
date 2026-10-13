import typer

from .extract import extract

app = typer.Typer()


@app.command()
def main(question: str, models: str = "qwen3.5:2b,qwen3.5:4b"):
    """Ask every model the same question and print JSON plus latency."""
    for model in models.split(","):
        result, latency = extract(question, model)
        print(f"{model} ({latency:.0f} ms)")
        print(result.model_dump_json(indent=2))
