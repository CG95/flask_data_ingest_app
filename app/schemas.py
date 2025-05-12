from marshmallow import Schema, fields, validate

class SaleSchema(Schema):
    month = fields.DateTime()
    total_quantity = fields.Integer()
    total_revenue = fields.Decimal(as_string=True)

class TopRevenueProductSchema(Schema):
    product_name = fields.String()
    total_revenue = fields.Decimal(as_string=True)

