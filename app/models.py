import click
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy, event
from sqlalchemy.engine import Engine
from sqlalchemy.sql import func, and_, extract


db = SQLAlchemy()


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
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
        db.ForeignKey('categories.id', onupdate='CASCADE', ondelete='SET NULL'),
        default=1
    )
    category = db.relationship('Category')

    def __repr__(self):
        return f'<Transaction {self.id}; {self.account_date} {self.amount:.2f} @ {self.category.name}>'


class ParentCategory(db.Model):
    __tablename__ = 'parent_categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

    def __repr__(self):
        return f'<ParentCategory {self.id} "{self.name}">'


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    parent_id = db.Column(
        db.Integer,
        db.ForeignKey('parent_categories.id', onupdate='CASCADE', ondelete='SET NULL')
    )
    parent = db.relationship('ParentCategory')

    def __repr__(self):
        return f'<Category {self.id} "{self.name}">'


class Budget(db.Model):
    __tablename__ = 'budgets'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    estimate = db.Column(db.Float, nullable=False)
    category_id = db.Column(
        db.Integer,
        db.ForeignKey('categories.id', onupdate='CASCADE', ondelete='SET NULL'),
        nullable=False
    )
    category = db.relationship('Category')

    def __repr__(self):
        return f'<Budget {self.id}; {self.date} {self.estimate} "{self.category}">'


def mock():
    from datetime import date, timedelta

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

    year = 2018
    month = 5

    print('Sub category summaries:')
    for parent in ParentCategory.query.all():
        print(parent.name + ':')
        q = db.session.query(
            Category.name, func.sum(Transaction.amount), Budget.estimate
        ).join(ParentCategory).join(Budget).join(Transaction).group_by(Category).filter(
            and_(
                ParentCategory.id == parent.id,
                extract('year', Transaction.account_date) == year,
                extract('month', Transaction.account_date) == month
            )
        )
        print(q.all())

    print('Main summary:')

    q = db.session.query(
        ParentCategory.name, func.sum(Transaction.amount).label('transaction_sum'), Budget.estimate
    ).join(Category).join(Budget).join(Transaction).group_by(ParentCategory).filter(
        and_(
            ParentCategory.id.isnot(None),
            extract('year', Transaction.account_date) == year,
            extract('month', Transaction.account_date) == month
        )
    ).subquery()

    q2 = db.session.query(
        q.c.name, func.sum(q.c.estimate), func.sum(q.c.transaction_sum)
    ).group_by(q.c.name)
    parent_category_summary = q2.all()

    q = db.session.query(
        Category.name, func.sum(Transaction.amount), Budget.estimate
    ).join(Transaction).join(Budget).group_by(Category.id).filter(
        and_(
            Category.parent_id.is_(None),
            extract('year', Transaction.account_date) == year,
            extract('month', Transaction.account_date) == month
        )
    )
    rest_category_summary = q.all()

    print(parent_category_summary + rest_category_summary)


def init_db():
    db.drop_all()
    db.create_all()

    category = Category(id=1, name='?')
    db.session.add(category)
    db.session.commit()


@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()

    click.echo('Initialized the database.')


@click.command('mock-db')
@with_appcontext
def mock_db_command():
    init_db()
    mock()
    click.echo('Mocked up the database.')
