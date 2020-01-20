from flask import request, abort
from flask_restplus import Resource, fields
from api.extensions import db, api
from api.models import Product 
from api.schemas import product_schema, products_schema

product_fields = api.model('Product', {
    'nome': fields.String(),
    'preco': fields.Float(),
    'preco_prime': fields.Float(),
    'preco_antigo': fields.Float(),
    'disponibilidade': fields.Boolean(),
    'preco_desconto': fields.Float(),
    'preco_desconto_prime': fields.Float(),
    'produto_prime': fields.Boolean()
})

@api.route('/product')
class ProductListResource(Resource):
    def get(self):
        all_products = Product.query.all()
        return products_schema.dump(all_products)
    
    @api.expect(product_fields) 
    def post(self):
        product = product_schema.load(request.json)
        db.session.add(product)
        db.session.commit()
        return product_schema.dump(product), 201   
  
@api.route('/product/<int:id>')
class ProductResource(Resource):
    def get(self, id):
        product = Product.query.get_or_404(id)
        return product_schema.dump(product)       
    
    @api.expect(product_fields) 
    def put(self, id):
        product = Product.query.get_or_404(id)
        product = product_schema.load(request.json, instance=product)
        db.session.add(product)
        db.session.commit()
        return product_schema.dump(product)

    def delete(self, id):
        product = Product.query.get_or_404(id)
        db.session.delete(product)
        db.session.commit()
        return '', 204
