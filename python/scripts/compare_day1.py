import csv
import json
import statistics
from pathlib import Path

from commerce_router.extract import extract

MODELS = ["qwen3.5:2b", "qwen3.5:4b"]
ROOT = Path(__file__).resolve().parent.parent  # the python/ folder
DATA = ROOT / "data" / "day1_questions.csv"
OUT = ROOT / "results" / "day1.jsonl"


def main() -> None:
    with DATA.open() as f:
        rows = list(csv.DictReader(f))  # each row: {"question": ..., "expected": ...}

    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w") as out:
        for model in MODELS:
            extract("warm up", model)  # loads the model so load time doesn't skew the numbers
            correct, latencies = 0, []
            for row in rows:
                result, ms = extract(row["question"], model)
                got = {intent.value for intent in result.intents}
                expected = set(row["expected"].split("|"))
                ok = got == expected
                correct += ok
                latencies.append(ms)
                out.write(
                    json.dumps(
                        {
                            "model": model,
                            "question": row["question"],
                            "expected": sorted(expected),
                            "got": sorted(got),
                            "ok": ok,
                            "ms": round(ms),
                            "details": result.model_dump(mode="json"),
                        }
                    )
                    + "\n"
                )
            print(f"{model} {correct}/{len(rows)} median {statistics.median(latencies):,.0f} ms")


if __name__ == "__main__":
    main()
