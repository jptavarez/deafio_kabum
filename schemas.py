from marshmallow_sqlalchemy import field_for
from flask_marshmallow.fields import fields
from extensions import ma
from models import Product

class ProductSchema(ma.ModelSchema):
    id = field_for(Product, 'id', dump_only=True)
    preco = fields.Float()
    preco_prime = fields.Float()
    preco_antigo = fields.Float()
    preco_desconto = fields.Float()
    preco_desconto_prime = fields.Float()

    class Meta:
        model = Product
    
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)