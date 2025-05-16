from marshmallow import Schema, fields, validate

class MonthlySaleSummarySchema(Schema):
    month = fields.DateTime()
    total_quantity = fields.Integer()
    total_revenue = fields.Decimal(as_string=True)

class TopRevenueProductSchema(Schema):
    product_id = fields.Integer()
    product_name = fields.String()
    total_revenue = fields.Decimal(as_string=True)

class SaleSummarySchema(Schema):
    region = fields.String()
    product_id = fields.Integer()
    product_name = fields.String()
    total_quantity = fields.Integer()
    total_revenue = fields.Decimal(as_string=True)
