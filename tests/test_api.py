from datetime import date
import pytest

from app.models import Category, Transaction


@pytest.mark.parametrize(
    'endpoint, length', [
        ('categories', 4)
    ]
)
def test_getting_resources(client, endpoint, length):
    rv = client.get(f'/api/{endpoint}')
    json_data = rv.get_json()

    assert len(json_data) == length


@pytest.mark.parametrize(
    'endpoint, fields', [
        ('categories', {'date', 'estimate', 'id', 'name'})
    ]
)
def test_getting_resource_id_fields(client, endpoint, fields):
    rv = client.get(f'/api/{endpoint}/1')
    json_data = rv.get_json()

    fields == set(json_data.keys())


@pytest.mark.parametrize(
    'endpoint', [
        ('categories'),
        ('parent-categories'),
        ('transactions'),
        ('budgets')
    ]
)
def test_getting_resource_wrong_id(client, endpoint):
    rv = client.get(f'/api/{endpoint}/999')
    json_data = rv.get_json()

    assert json_data['message'].startswith('The requested URL was not found on the server')


def test_posting_category(app, client):
    json_dict = {'name': 'Health', 'estimate': -300, 'date': '2018-05-01'}
    rv = client.post('/api/categories', json=json_dict)

    assert rv.status_code == 200


def test_putting_category(app, client):
    json_dict = {'name': 'some different name'}
    rv = client.put('/api/categories/1', json=json_dict)

    assert rv.status_code == 200

    with app.app_context():
        category = Category.query.filter_by(id=1).first()

    assert category.name == json_dict['name']


def test_deleting_category(app, client):
    with app.app_context():
        initial_count = len(Category.query.all())
        category = Category.query.filter_by(id=1).first()

    rv = client.delete('/api/categories/1')
    assert rv.status_code == 200

    with app.app_context():
        category = Category.query.filter_by(id=1).first()
        assert category is None

        assert len(Category.query.all()) == initial_count - 1

        assert len(Transaction.query.filter_by(category_id=1).all()) == 0
