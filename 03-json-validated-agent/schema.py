from pydantic import BaseModel, model_validator
from typing import List, Optional

class LineItem(BaseModel):
    description: str
    quantity: float
    price: float

class Invoice(BaseModel):
    invoice_number: Optional[str] = None
    date: Optional[str] = None
    vendor_name: str
    line_items: List[LineItem]
    total_amount: Optional[float] = None
    total_mismatch: Optional[bool] = None

    @model_validator(mode="after")
    def flag_total_mismatch(self):
        if self.total_amount is not None:
            calculated = sum(item.quantity * item.price for item in self.line_items)
            self.total_mismatch = abs(calculated - self.total_amount) > 0.01
        else:
            self.total_mismatch = None
        return self