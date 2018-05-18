import pytest
from datetime import date, timedelta

from app import create_app
from app.models import db, Category, Transaction


@pytest.fixture
def app():
    test_config = {
        'TESTING': True,
        'SECRET_KEY': 'testing',
        'SQLALCHEMY_DATABASE_URI': 'sqlite://',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    }

    # store the database in the instance folder
    app = create_app(test_config=test_config)

    with app.app_context():
        db.create_all()
        create_test_data(db)

    return app


@pytest.fixture
def client(app):
    return app.test_client()


def create_test_data(db):

    for name in ['?', 'Car', 'Grocery']:
        category = Category(
            name=name,
            date=date(2018, 5, 1),
            estimate=-12.34
        )

        db.session.add(category)

    db.session.commit()

    categories = Category.query.all()

    for i in range(30):
        transaction = Transaction(
            account_date=date(2018, 5, 1) + timedelta(days=i),
            category=categories[i % 3],
            amount=-12.34
        )

        db.session.add(transaction)

    db.session.commit()
