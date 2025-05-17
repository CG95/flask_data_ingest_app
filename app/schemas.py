from marshmallow import Schema, fields, validate

class MonthlySaleSummarySchema(Schema):
    month = fields.DateTime()
    total_quantity = fields.Integer()
    total_revenue = fields.Decimal(as_string=True)

class MonthlySaleSummaryResponseSchema(Schema):
    data = fields.List(fields.Nested(MonthlySaleSummarySchema))
    duration = fields.Float()

class TopRevenueProductSchema(Schema):
    product_id = fields.Integer()
    product_name = fields.String()
    total_revenue = fields.Decimal(as_string=True)
    
class TopRevenueProductResponseSchema(Schema):
    data = fields.List(fields.Nested(TopRevenueProductSchema))
    duration = fields.Float()    

class SaleSummarySchema(Schema):
    region = fields.String()
    product_id = fields.Integer()
    product_name = fields.String()
    total_quantity = fields.Integer()
    total_revenue = fields.Decimal(as_string=True)

class SaleSummaryResponseSchema(Schema):
    data = fields.List(fields.Nested(SaleSummarySchema))
    duration = fields.Float()

class ErrorSchema(Schema):
    message = fields.String()