from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel

app = FastAPI()

products_db = [
    {"id": 101, "name": "Bàn phím cơ", "stock": 5, "price": 1200000.0},
    {"id": 102, "name": "Chuột Gaming", "stock": 2, "price": 600000.0},
]
orders_db = []


class OrderCreate(BaseModel):
    product_id: int
    quantity: int


@app.post("/orders", status=status.HTTP_201_CREATED)
def create_order(order=OrderCreate):
    if order.quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Số lượng mua phải lớn hơn 0",
        )

    for p in products_db:
        if p["id"] == order.product_id:
            if order.quantity > p["stock"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Sản phẩm không đủ số lượng trong kho",
                )

        p["stock"] -= order.quantity
        new_oder = {
            "id": len(orders_db) + 1 if len(orders_db) > 0 else 1,
            **order.model_dump(),
            "total_price": order["quantity"] * p["price"],
        }
        orders_db.append(new_oder)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Sản phẩm không tồn tại"
    )
