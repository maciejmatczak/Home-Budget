from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource
from marshmallow import Schema, fields, post_load

from .models import db, Category, Transaction

bp = Blueprint('api', __name__)
api = Api(bp)


class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    date = fields.Date(required=True)
    estimate = fields.Float(required=True)

    @post_load
    def make_model(self, data):
        return Category(**data)


category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)


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
    def get(self, id):
        transaction = Transaction.query.get_or_404(id)
        return jsonify({
            'transaction': transaction
        })

    def post(self):
        pass


class TransactionResource(Resource):
    def get(self, id):
        transaction = Transaction.query.get_or_404(id)
        return jsonify({
            'transaction': transaction
        })

    def put(self, id):
        pass

    def delete(self, id):
        pass


api.add_resource(CategoryResource, '/categories/<int:id>')
api.add_resource(CategoryListResource, '/categories')
api.add_resource(TransactionResource, '/transactions/<int:id>')
