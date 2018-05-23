import click
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy, event
from sqlalchemy.engine import Engine


db = SQLAlchemy()


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    estimate = db.Column(db.Float, nullable=False)


# class SubCategory(db.Model):
#     __tablename__ = 'subcategories'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, nullable=False)
#     date = db.Column(db.Date, nullable=False)
#     estimate = db.Column(db.Float, nullable=False)
#     category_id = db.Column(
#         db.Integer,
#         db.ForeignKey('categories.id', onupdate='CASCADE', ondelete='SET NULL')
#     )
#     category = db.relationship('Category', backref='subcategories')


class BudgetRule(db.Model):
    __tablename__ = 'budget_rules'
    id = db.Column(db.Integer, primary_key=True)
    sentence = db.Column(db.String, nullable=False)
    estimate = db.Column(db.Float, nullable=False)
    category_id = db.Column(
        db.Integer,
        db.ForeignKey('categories.id', onupdate='CASCADE', ondelete='SET NULL')
    )
    category = db.relationship('Category')


class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    new = db.Column(db.Boolean)
    account_date = db.Column(db.Date, nullable=False)
    operation_date = db.Column(db.Date)
    details = db.Column(db.String)
    account_no = db.Column(db.String)
    title = db.Column(db.String)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String)
    ref_number = db.Column(db.String)
    operation_type = db.Column(db.String)
    note = db.Column(db.String)
    category_id = db.Column(
        db.Integer,
        db.ForeignKey('categories.id', onupdate='CASCADE', ondelete='SET NULL')
    )
    category = db.relationship('Category')


def mockup(db):
    from datetime import date, timedelta
    import random

    for name in ['?', 'Car', 'Grocery']:
        category = Category(
            name=name,
            estimate=-12.34
        )

        db.session.add(category)

    db.session.commit()

    categories = Category.query.all()

    for i in range(30):
        transaction = Transaction(
            account_date=date(2018, 5, 1) + timedelta(days=i),
            category=random.choice(categories),
            amount=-12.34
        )

        db.session.add(transaction)

    db.session.commit()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    db.drop_all()
    db.create_all()
    click.echo('Initialized the database.')


@click.command('mock-db')
@with_appcontext
def mock_db_command():
    mockup(db)
    click.echo('Mocked up the database.')
