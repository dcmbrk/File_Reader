from pydantic import BaseModel
from pydantic import BaseModel, Field
from typing import List

class Invoice(BaseModel):
    items: List[InvoiceItem] = Field(..., description="List of individual line items in the invoice")
    summary: InvoiceSummary = Field(..., description="Summary of totals and tax information")

class InvoiceItem(BaseModel):
    item_no: int = Field(..., alias="Col1", description="Line item sequence number")
    description: str = Field(..., alias="Tên hàng hóa, dịch vụ", description="Detailed description of goods or services")
    unit: str = Field(..., alias="Đơn vị tính", description="Unit of measurement (e.g., pcs, set, kg)")
    quantity: int = Field(..., alias="Số lượng", description="Quantity of items")
    unit_price: float = Field(..., alias="Đơn giá", description="Price per unit")
    total_amount: float = Field(..., alias="Col6", description="Line item total amount excluding tax")

class InvoiceSummary(BaseModel):
    sub_total: float = Field(..., description="Total amount before VAT")
    vat_rate: str = Field(..., description="Value Added Tax rate (e.g., 8%, 10%)")
    vat_amount: float = Field(..., description="Total VAT tax amount")
    total_payment: float = Field(..., description="Final total payment amount including tax")