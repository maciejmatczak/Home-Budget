from flask import Blueprint, jsonify
from flask_restful import Api, Resource, fields, marshal_with

from .models import Category, Transaction

bp = Blueprint('api', __name__)
api = Api(bp)


category_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'date': fields.String,
    'estimate': fields.Float
}


class CategoryResource(Resource):
    @marshal_with(category_fields)
    def get(self, id):
        category = Category.query.get_or_404(id)
        return category


class CategoryListResource(Resource):
    @marshal_with(category_fields)
    def get(self):
        categories = Category.query.all()
        return categories


class TransactionResource(Resource):
    def get(self, id):
        transaction = Transaction.query.get_or_404(id)
        return jsonify({
            'transaction': transaction
        })


api.add_resource(CategoryResource, '/categories/<int:id>')
api.add_resource(CategoryListResource, '/categories')
api.add_resource(TransactionResource, '/transactions/<int:id>')
