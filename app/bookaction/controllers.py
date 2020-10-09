from app import db
from .book_action_model import BookAction, BookActionName
from . import bookaction
from app.catalog.book_model import Book
from flask import request, abort, jsonify
from sqlalchemy.exc import SQLAlchemyError


@bookaction.errorhandler(AssertionError)
def validation_error(e):
    return jsonify({'error': str(e)}), 404


@bookaction.errorhandler(SQLAlchemyError)
def database_error(e):
    db.session.rollback()
    return jsonify({
        'error': 'Internal server error'
    }), 500


@bookaction.errorhandler(404)
def not_found(e):
    return jsonify(error=str(e)), 404


@bookaction.route('/receive/<int:book_id>', methods=['POST'])
def receive(book_id):
    if not Book.query.get(book_id):
        abort(404, 'Book does not exist')

    data = request.get_json()
    action = BookAction(
        BookActionName.RECEIVE,
        data.get('copies'),
        book_id=book_id,
        comment=data.get('comment')
    )
    action.save()

    return '', 201
