from flask import Blueprint, request
from flask_restful import Api, Resource
from marshmallow import Schema, fields, post_load

from app.models import db, Category, ParentCategory, Budget, Transaction

bp = Blueprint('api', __name__)
api = Api(bp)


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
    category = fields.Nested('CategorySchema', dump_only=True)
    category_id = fields.Integer()

    @post_load
    def make_model(self, data):
        return Transaction(**data)


transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)


class ParentCategorySchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)

    @post_load
    def make_model(self, data):
        return ParentCategory(**data)


parent_category_schema = ParentCategorySchema()
parent_categories_schema = ParentCategorySchema(many=True)


class CategorySchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    parent = fields.Nested(ParentCategorySchema)

    @post_load
    def make_model(self, data):
        return Category(**data)


category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)


class BudgetSchema(Schema):
    id = fields.Integer(dump_only=True)
    date = fields.Date(required=True)
    estimate = fields.Float(required=True)
    category = fields.Nested(CategorySchema, required=True)

    @post_load
    def make_model(self, data):
        return Budget(**data)


budget_schema = BudgetSchema()
budgets_schema = BudgetSchema(many=True)


class CategoryListResource(Resource):
    def get(self):
        item = Category.query.all()
        result = categories_schema.dump(item)

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
        updated_item, _ = category_schema.load(json)

        category = Category.query.get_or_404(id)
        for attr, value in json.items():
            setattr(category, attr, value)

        db.session.commit()

    def delete(self, id):
        category = Category.query.get_or_404(id)
        db.session.delete(category)
        db.session.commit()


class ParentCategoryListResource(Resource):
    def get(self):
        item = ParentCategory.query.all()
        result = parent_categories_schema.dump(item)

        return result

    def post(self):
        json = request.get_json()
        result = parent_category_schema.load(json)

        db.session.add(result.data)
        db.session.commit()


class ParentCategoryResource(Resource):
    def get(self, id):
        item = ParentCategory.query.get_or_404(id)
        result = parent_category_schema.dump(item)

        return result

    def put(self, id):
        json = request.get_json()
        new_data, _ = parent_category_schema.load(json)

        item = ParentCategory.query.get_or_404(id)
        for attr, value in json.items():
            setattr(item, attr, value)

        db.session.commit()

    def delete(self, id):
        item = ParentCategory.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()


class TransactionListResource(Resource):
    def get(self):
        item = Transaction.query.all()
        result = transactions_schema.dump(item)

        return result

    def post(self):
        json = request.get_json()
        result = transaction_schema.load(json)

        db.session.add(result.data)
        db.session.commit()


class TransactionResource(Resource):
    def get(self, id):
        item = Transaction.query.get_or_404(id)
        result = transaction_schema.dump(item)

        return result

    def put(self, id):
        json = request.get_json()
        new_data, _ = transaction_schema.load(json)

        item = Transaction.query.get_or_404(id)
        for attr, value in json.items():
            setattr(item, attr, value)

        db.session.commit()

    def delete(self, id):
        item = Transaction.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()


class BudgetListResource(Resource):
    def get(self):
        item = Budget.query.all()
        result = budgets_schema.dump(item)

        return result

    def post(self):
        json = request.get_json()
        result = budget_schema.load(json)

        db.session.add(result.data)
        db.session.commit()


class BudgetResource(Resource):
    def get(self, id):
        item = Budget.query.get_or_404(id)
        result = budget_schema.dump(item)

        return result

    def put(self, id):
        json = request.get_json()
        new_data, _ = budget_schema.load(json)

        item = Budget.query.get_or_404(id)
        for attr, value in json.items():
            setattr(item, attr, value)

        db.session.commit()

    def delete(self, id):
        item = Budget.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()


api.add_resource(CategoryResource, '/categories/<int:id>')
api.add_resource(CategoryListResource, '/categories')
api.add_resource(ParentCategoryResource, '/parent-categories/<int:id>')
api.add_resource(ParentCategoryListResource, '/parent-categories')
api.add_resource(BudgetResource, '/budgets/<int:id>')
api.add_resource(BudgetListResource, '/budgets')
api.add_resource(TransactionResource, '/transactions/<int:id>')
api.add_resource(TransactionListResource, '/transactions')
