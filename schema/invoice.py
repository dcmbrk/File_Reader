from pydantic import BaseModel
from pydantic import BaseModel, Field
from typing import List

class Invoice(BaseModel):
    items: List[InvoiceItem]
    summary: InvoiceSummary

class InvoiceItem(BaseModel):
    item_no: int = Field(..., alias="Col1")
    description: str = Field(..., alias="Tên hàng hóa, dịch vụ")
    unit: str = Field(..., alias="Đơn vị tính")
    quantity: int = Field(..., alias="Số lượng")
    unit_price: float = Field(..., alias="Đơn giá")
    total_amount: float = Field(..., alias="Col6")

class InvoiceSummary(BaseModel):
    sub_total: float = Field(..., description="Cộng tiền hàng")
    vat_rate: str = Field(..., description="Thuế suất GTGT (e.g., 8%)")
    vat_amount: float = Field(..., description="Tiền thuế GTGT")
    total_payment: float = Field(..., description="Tổng tiền thanh toán")
