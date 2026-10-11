import time
from datetime import date
from ollama import chat
from .schema import ShopperRequest

# Today's date lets the model turn "by Friday" into a number of days.
SYSTEM = f"""You convert shopper questions into JSON for a commerce router.
Today is {date.today():%A %Y-%m-%d}.
Intents:
- product_search: TODO one-line meaning + short example
- stock_check: TODO
- order_status: TODO
- delivery_promise: TODO
- other: anything else (policies, complaints, site problems)
A question can have several intents. Return only JSON that matches the schema."""

def extract(question: str, model: str) -> tuple[ShopperRequest, float]:
    start = time.perf_counter()
    response = chat(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": question},
        ],
        format=ShopperRequest.model_json_schema(),  # constrains output to your schema
        options={"temperature": 0},                 # same input -> same output; best for extraction
        think=False,                                # Qwen 3.5 thinks by default; we measured that it's slow
    )
    ms = (time.perf_counter() - start) * 1000
    result = ShopperRequest.model_validate_json(response.message.content)
    return result, ms
