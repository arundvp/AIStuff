from datetime import date
from types import SimpleNamespace

import pytest

from commerce_router import extract as extract_module
from commerce_router.schema import Intent, ShopperRequest

# What a good model reply looks like for "Red shoes to Boston in 2 days?"
CANNED_REPLY = (
    '{"intents": ["product_search", "delivery_promise"], "category": "shoes", "color": "red",'
    ' "destination_city": "Boston", "deadline_days": 2, "confidence": 0.9}'
)


@pytest.fixture
def sent(monkeypatch):
    """Replace ollama's chat() with a fake that records each call and returns CANNED_REPLY."""
    calls = []

    def fake_chat(**kwargs):
        calls.append(kwargs)
        return SimpleNamespace(message=SimpleNamespace(content=CANNED_REPLY))

    monkeypatch.setattr(extract_module, "chat", fake_chat)
    return calls


def test_extract_parses_the_reply(sent):
    result, ms = extract_module.extract("Red shoes to Boston in 2 days?", "fake-model")

    assert result.intents == [Intent.PRODUCT_SEARCH, Intent.DELIVERY_PROMISE]
    assert result.destination_city == "Boston"
    assert result.deadline_days == 2
    assert ms >= 0


def test_extract_sends_schema_date_and_settings(sent):
    extract_module.extract("Where is my order 48213?", "fake-model")
    call = sent[0]  # the keyword arguments extract() passed to chat()

    # 1. the right model
    assert call["model"] == "fake-model"
    # 2. the reply is held to the ShopperRequest schema
    assert call["format"] == ShopperRequest.model_json_schema()
    # 3. deterministic output, no hidden reasoning
    assert call["options"]["temperature"] == 0
    assert call["think"] is False
    # 4 and 5. exactly two messages: system (with today's date), then the user's question
    system, user = call["messages"]
    assert system["role"] == "system"
    assert date.today().isoformat() in system["content"]
    assert user == {"role": "user", "content": "Where is my order 48213?"}
