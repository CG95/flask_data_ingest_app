from . import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Index
from werkzeug.security import generate_password_hash, check_password_hash

"""
row samples
Sale_id,Product_id,Product_name,quantity,price,sale_date,customer_id,region
1,98,Action Figure PeachPuff,7,25.04,2024-10-17,1864,Hungary
1,66,Sunglasses BlueViolet,8,205.44,2024-10-17,1864,Hungary
"""

class Sales(db.Model):
    __tablename__ = 'sales'
    id= db.Column(db.Integer, primary_key=True)
    sale_id= db.Column(db.Integer, nullable=False)
    product_id= db.Column(db.Integer, nullable=False)
    product_name= db.Column(db.String(255), nullable=False)
    quantity= db.Column(db.Integer, nullable=False)
    price= db.Column(db.Numeric(10,2), nullable=False)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())
    customer_id = db.Column(db.Integer, nullable=False)
    region = db.Column(db.String(100), nullable=False)
    created_at= db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at= db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    @property
    def revenue(self):
        return self.quantity * self.price
    
Index('idx_product_date', Sales.product_id, Sales.date)
Index('idx_region_date', Sales.region, Sales.date)
