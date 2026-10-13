import pytest
from pydantic import ValidationError

from commerce_router.schema import Intent, ShopperRequest


def test_intent_values_are_the_router_contract():
    # If someone renames an intent, every later sub-agent breaks. This test catches it.
    assert {intent.value for intent in Intent} == {
        "product_search",
        "stock_check",
        "order_status",
        "delivery_promise",
        "other",
    }


def test_missing_details_default_to_none():
    req = ShopperRequest.model_validate_json('{"intents": ["order_status"], "confidence": 0.9}')
    assert req.intents == [Intent.ORDER_STATUS]
    assert req.order_id is None
    assert req.deadline_days is None


def test_confidence_above_1_is_rejected():
    with pytest.raises(ValidationError):
        ShopperRequest(intents=[Intent.OTHER], confidence=1.5)


def test_unknown_intent_is_rejected():
    with pytest.raises(ValidationError):
        ShopperRequest.model_validate_json('{"intents": ["teleport"], "confidence": 0.5}')
