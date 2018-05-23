from flask import Blueprint, request
from flask_restful import Api, Resource
from marshmallow import Schema, fields, post_load

from .models import db, Category, Transaction

bp = Blueprint('api', __name__)
api = Api(bp)


class CategorySchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    date = fields.Date(required=True)
    estimate = fields.Float(required=True)

    @post_load
    def make_model(self, data):
        return Category(**data)


category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)


class TransactionSchema(Schema):
    id = fields.Int(dump_only=True)
    new = fields.Boolean()
    account_date = fields.Date(required=True)
    operation_date = fields.Date()
    details = fields.String()
    account_no = fields.String()
    title = fields.String()
    amount = fields.Float(required=True)
    currency = fields.String()
    ref_number = fields.String()
    operation_type = fields.String()
    note = fields.String()
    category = fields.Nested(CategorySchema, dump_only=True)
    category_id = fields.Integer()

    @post_load
    def make_model(self, data):
        return Transaction(**data)


transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)


class CategoryListResource(Resource):
    def get(self):
        categories = Category.query.all()
        result = categories_schema.dump(categories)

        return result

    def post(self):
        json = request.get_json()
        result = category_schema.load(json)

        db.session.add(result.data)
        db.session.commit()


class CategoryResource(Resource):
    def get(self, id):
        category = Category.query.get_or_404(id)
        result = category_schema.dump(category)

        return result

    def put(self, id):
        json = request.get_json()
        new_data, _ = category_schema.load(json)

        category = Category.query.get_or_404(id)
        for attr, value in new_data.items():
            setattr(category, attr, value)

        db.session.commit()

    def delete(self, id):
        category = Category.query.get_or_404(id)
        db.session.delete(category)
        db.session.commit()


class TransactionListResource(Resource):
    def get(self):
        transactions = Transaction.query.all()
        result = transactions_schema.dump(transactions)

        return result

    def post(self):
        json = request.get_json()
        result = transaction_schema.load(json)

        db.session.add(result.data)
        db.session.commit()


class TransactionResource(Resource):
    def get(self, id):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass


api.add_resource(CategoryResource, '/categories/<int:id>')
api.add_resource(CategoryListResource, '/categories')
api.add_resource(TransactionResource, '/transactions/<int:id>')
api.add_resource(TransactionListResource, '/transactions')
