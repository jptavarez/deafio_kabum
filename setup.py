import json
from urllib import request
from app import app, db
from models import Product

with app.app_context():
    db.create_all()
    urls = [
        'https://servicespub.prod.api.aws.grupokabum.com.br/descricao/v1/descricao/produto/85197',
        'https://servicespub.prod.api.aws.grupokabum.com.br/descricao/v1/descricao/produto/79936',
        'https://servicespub.prod.api.aws.grupokabum.com.br/descricao/v1/descricao/produto/87400'
    ]

    for url in urls:
        with request.urlopen(url) as url:
            data = json.loads(url.read().decode())
            products = data['familia']['produtos']
            for product in products:
                product.pop('link_descricao')
                product.pop('foto')
                product['id'] = product.pop('codigo')
                obj = Product(**product)
                db.session.add(obj)
    db.session.commit()


