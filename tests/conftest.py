import pytest
from datetime import date, timedelta

from app import create_app
from app.models import db, Category, ParentCategory, Budget, Transaction


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
    bills = ParentCategory(
        name='Bills'
    )

    db.session.add(bills)

    categories = {
        'Car': None,
        'Grocery': None,
        'TV Multimedia Internet': bills,
        'Flat rent': bills,
    }
    for name, parent in categories.items():
        category = Category(
            name=name,
            parent=parent
        )

        db.session.add(category)

    categories = Category.query.all()

    for i in range(30):
        transaction = Transaction(
            account_date=date(2018, 5, 1) + timedelta(days=i),
            category=categories[i % len(categories)],
            amount=-10
        )

        db.session.add(transaction)

    for category in categories:
        budget = Budget(
            category=category,
            date=date(2018, 5, 1),
            estimate=-100
        )

        db.session.add(budget)

    db.session.commit()
