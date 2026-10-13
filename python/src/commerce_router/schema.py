from enum import StrEnum

from pydantic import BaseModel, Field


class Intent(StrEnum):
    PRODUCT_SEARCH = "product_search"
    STOCK_CHECK = "stock_check"
    ORDER_STATUS = "order_status"
    DELIVERY_PROMISE = "delivery_promise"
    OTHER = "other"


class ShopperRequest(BaseModel):
    intents: list[Intent] = Field(description="Every intent in the question, most important first")
    category: str | None = Field(None, description="Product type, e.g. 'shoes'")
    color: str | None = Field(None, description="Main color asked for, lowercase, e.g. 'red'")
    size: str | None = Field(
        None, description="Size as the shopper wrote it, e.g. '9', 'M', '10.5'"
    )
    budget_max: float | None = Field(
        None, description="Highest price the shopper will pay, number only, e.g. 80"
    )
    destination_city: str | None = Field(
        None, description="City the item must be delivered to, e.g. 'Boston'"
    )
    deadline_days: int | None = Field(
        None,
        description="Whole days from today until the item must arrive, e.g. 2; convert weekdays like 'by Friday' using today's date",
    )
    order_id: str | None = Field(
        None, description="Order number exactly as written, e.g. '48213' or 'A-1009'"
    )
    confidence: float = Field(ge=0, le=1, description="How sure you are about the intents, 0 to 1")
