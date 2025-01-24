from pydantic import BaseModel, ConfigDict


class ProductBaseSchema(BaseModel):
    article: int


class ProductSchema(ProductBaseSchema):
    name: str
    price: float
    price_sale: float | None
    rating: int | None
    total_quantity: int

    model_config = ConfigDict(from_attributes=True)
