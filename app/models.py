from . import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Index


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

#    @property
#    def revenue(self):
#        return self.quantity * self.price



