from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate

def create_product(db:Session,product:ProductCreate,user_id:int):
    db_product=Product(**product.dict(),owner_id=user_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(db:Session,skip:int=0,limit:int=10):
    return db.query(Product).offset(skip).limit(limit).all()

def get_product(db:Session, product_id:int):
    return db.query(Product).filter(Product.id==product_id).first()

def delete_product(db:Session,product_id:int,user_id:int,is_admin:bool=False):
    product=get_product(db,product_id)
    if product is None or (not is_admin and product.owner_id != user_id):
        return None
    db.delete(product)
    db.commit()
    return product