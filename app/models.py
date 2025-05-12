from . import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Index
from werkzeug.security import generate_password_hash, check_password_hash

class Sales(db.Model):
    __tablename__ = 'sales'
    id= db.Column(db.Integer, primary_key=True)
    product_name= db.Column(db.String(50), nullable=False)
    quantity= db.Column(db.Integer, nullable=False)
    price= db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())
    customer_id = db.Column(db.Integer, nullable=False)
    created_at= db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at= db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    @property
    def revenue(self):
        return self.quantity * self.price
    
Index('idx_product_date', Sales.product, Sales.date)
Index('idx_region_date', Sales.region, Sales.date)
