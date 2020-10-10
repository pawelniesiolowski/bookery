from app import db
from .book_action_model import BookAction, BookActionName
from . import bookaction
from flask import request, abort, jsonify
from sqlalchemy.exc import SQLAlchemyError
from app.catalog.services import BookService


@bookaction.errorhandler(AssertionError)
def validation_error(e):
    error = {
        'error': str(e),
        'status': 400
    }
    return jsonify(error), 400


@bookaction.errorhandler(SQLAlchemyError)
def database_error(e):
    db.session.rollback()
    return jsonify({
        'error': 'Internal server error',
        'status': 500
    }), 500


@bookaction.errorhandler(404)
def not_found(e):
    error = {
        'error': str(e),
        'status': 404
    }
    return jsonify(error), 404


@bookaction.route('/receive/<int:book_id>', methods=['POST'])
def receive(book_id):
    if not BookService().does_book_exist(book_id):
        abort(404, 'Taka książka nie istnieje w katalogu')

    data = request.get_json()
    action = BookAction(
        BookActionName.RECEIVE,
        int(data.get('copies')),
        book_id=int(book_id),
        comment=data.get('comment')
    )
    action.save()

    return jsonify({'message': '', 'status': 201}), 201
