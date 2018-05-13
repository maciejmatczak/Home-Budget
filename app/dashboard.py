from datetime import datetime

from flask import Blueprint, redirect, render_template, url_for

bp = Blueprint('dashboard', __name__)


@bp.route('/<month>')
def month_view(month):
    #     db = get_db()
    #     cursor = db.execute(
    #         '''
    #         select transactions.id, account_date, amount, name
    #         from transactions
    #         join categories
    #         on transactions.category_id = categories.id
    #         where strftime('%m', account_date) = ?
    #         ''',
    #         (month,)
    #     )
    #     transactions = cursor.fetchall()
    #     transactions_cols = [description[0] for description in cursor.description]

    # if not month:
    #     month = [''] * 4

    # cursor = db.execute(
    #     '''
    #     select id, name, date, estimate
    #     from categories
    #     '''
    # )

    # categories = cursor.fetchall()
    # categories_cols = [description[0] for description in cursor.description]

    # if not categories:
    #     categories = [''] * 4

    return render_template(
        'dashboard/index.html',
        transactions_columns=None,
        transactions_rows=None,
        categories_columns=None,
        categories_rows=None
    )


@bp.route('/')
def index():

    return redirect(url_for('.month_view', month=datetime.now().strftime('%m')))
