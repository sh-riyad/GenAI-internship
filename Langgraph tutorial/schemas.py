from pydantic import BaseModel
import datetime


class StoreProductInput(BaseModel):
    name: str
    product_code: str
    price: float
    expiry_date: datetime.date
    brand: str
    product_type: str

    class Config:
        from_attributes = True

class StoreServiceInput(BaseModel):
    name: str
    service_code: str
    price: float

    class Config:
        from_attributes = True