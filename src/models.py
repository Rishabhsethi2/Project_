from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional

class MarketTick(BaseModel):
    """
    The strict Data Contract for all historical market data entering the system.
    If the data does not mathematically match this schema, it is rejected before hitting Postgres.
    """
    symbol: str = Field(..., description="The ticker symbol (e.g., RELIANCE.NS)")
    trade_date: datetime = Field(..., description="The date of the market data")
    open_price: float = Field(..., ge=0, description="Opening price")
    high_price: float = Field(..., ge=0, description="Highest price of the day")
    low_price: float = Field(..., ge=0, description="Lowest price of the day")
    close_price: float = Field(..., ge=0, description="Closing price")
    volume: int = Field(..., ge=0, description="Total shares traded")

    @field_validator('high_price')
    def high_must_be_highest(cls, v, info):
        """Mathematical validation: High must be >= Low"""
        if 'low_price' in info.data and v < info.data['low_price']:
            raise ValueError("High price cannot be lower than Low price.")
        return v