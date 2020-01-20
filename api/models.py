from api.extensions import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    preco = db.Column(db.Float(5, 2), nullable=False)
    preco_prime = db.Column(db.Float(5, 2), nullable=False)
    preco_antigo = db.Column(db.Float(5, 2), nullable=False)
    disponibilidade = db.Column(db.Boolean, default=False)
    preco_desconto = db.Column(db.Float(5, 2), nullable=False)
    preco_desconto_prime = db.Column(db.Float(5, 2), nullable=False)
    produto_prime = db.Column(db.Boolean, default=False)