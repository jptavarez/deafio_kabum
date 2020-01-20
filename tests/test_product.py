import os
import tempfile
import pytest
from api.app import app, db
from api.models import Product

@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db_test.sqlite')
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()                     
        yield client
    os.close(db_fd)
    os.unlink(app.config['DATABASE'])    

nome = 'Teste Produto'
preco = 100.90
preco_prime = 90.90
preco_antigo = 150.85
disponibilidade = True
preco_desconto = 85.90
preco_desconto_prime = 80.89
produto_prime = True 

def test_create_product(client):
    response = _create_product(client)
    data = response.get_json()
    assert response.status_code == 201, 'Erro ao criar o produto'
    assert data['nome'] == nome, 'Nome retornado inválido'
    assert data['preco'] == preco, 'preco retornado inválido'
    assert data['preco_prime'] == preco_prime, 'preco_prime retornado inválido'
    assert data['disponibilidade'] == disponibilidade, 'disponibilidade retornado inválido'
    assert data['preco_desconto'] == preco_desconto, 'preco_desconto retornado inválido'
    assert data['preco_desconto_prime'] == preco_desconto_prime, 'preco_desconto_prime retornado inválido'
    assert data['produto_prime'] == produto_prime, 'produto_prime retornado inválido'

def test_update_product(client):
    response = _create_product(client)
    data = response.get_json()
    id = data['id']
    response = client.put('/product/' + str(id), json={
        'nome': nome + ' atualizado',
        'preco': preco,
        'preco_prime': preco_prime,
        'preco_antigo': preco_antigo,
        'disponibilidade': disponibilidade,
        'preco_desconto': preco_desconto,
        'preco_desconto_prime': preco_desconto_prime,
        'produto_prime': produto_prime
    })
    data = response.get_json()
    assert response.status_code == 200, 'Erro ao atualizar o produto'
    assert data['nome'] == nome + ' atualizado', 'Erro ao atualizar o produto'

def test_get_product(client):
    response = _create_product(client)
    data = response.get_json()
    id = data['id']
    response = client.get('/product/' + str(id))
    assert response.status_code == 200, 'Erro ao buscar o produto'
    assert 'nome' in data, 'nome não esta presente no json retornado'
    assert 'preco' in data, 'preco não esta presente no json retornado'
    assert 'preco_prime' in data, 'preco_prime não esta presente no json retornado'
    assert 'disponibilidade' in data, 'disponibilidade não esta presente no json retornado'
    assert 'preco_desconto' in data, 'preco_desconto não esta presente no json retornado'
    assert 'preco_desconto_prime' in data, 'preco_desconto_prime não esta presente no json retornado'
    assert 'produto_prime' in data, 'produto_prime não esta presente no json retornado'

def test_delete_product(client):
    response = _create_product(client)
    data = response.get_json()
    id = data['id']
    response = client.delete('/product/' + str(id))
    assert response.status_code == 204, 'Erro ao deletar o produto'

def test_list_all_products(client):
    _create_product(client)
    _create_product(client)
    response = client.get('/product')
    data = response.get_json()
    assert response.status_code == 200, 'Erro ao buscar os produto'
    assert len(data) == 2, 'Qtd de produtos retornados inválida'

def _create_product(client):       
    response = client.post('/product', json={
        'nome': nome,
        'preco': preco,
        'preco_prime': preco_prime,
        'preco_antigo': preco_antigo,
        'disponibilidade': disponibilidade,
        'preco_desconto': preco_desconto,
        'preco_desconto_prime': preco_desconto_prime,
        'produto_prime': produto_prime
    })
    return response

