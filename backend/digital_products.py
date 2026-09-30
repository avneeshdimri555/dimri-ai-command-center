from typing import Any
from uuid import uuid4
from .db import connect, now

def init_product_table():
    with connect() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS digital_products (
            id TEXT PRIMARY KEY, title TEXT NOT NULL, product_type TEXT NOT NULL,
            description TEXT, price REAL, currency TEXT, asset_path TEXT,
            status TEXT NOT NULL, target_marketplaces TEXT, created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )""")
init_product_table()

def create_product(title: str, product_type: str, description: str = "", price: float | None = None,
                   currency: str = "USD", asset_path: str | None = None, marketplaces: str = "gumroad") -> dict[str, Any]:
    item={"id":f"dp-{uuid4().hex[:10]}","title":title,"product_type":product_type,"description":description,
          "price":price,"currency":currency,"asset_path":asset_path,"status":"draft",
          "target_marketplaces":marketplaces,"created_at":now(),"updated_at":now()}
    with connect() as conn:
        conn.execute("INSERT INTO digital_products VALUES (:id,:title,:product_type,:description,:price,:currency,:asset_path,:status,:target_marketplaces,:created_at,:updated_at)",item)
    return item

def list_products():
    with connect() as conn:
        return [dict(r) for r in conn.execute("SELECT * FROM digital_products ORDER BY created_at DESC LIMIT 200")]

def publish_plan(product_id: str):
    with connect() as conn:
        row=conn.execute("SELECT * FROM digital_products WHERE id=?",(product_id,)).fetchone()
        if not row: return None
        item=dict(row)
        conn.execute("UPDATE digital_products SET status=?,updated_at=? WHERE id=?",("approval_required",now(),product_id))
        item["status"]="approval_required"
        return item
