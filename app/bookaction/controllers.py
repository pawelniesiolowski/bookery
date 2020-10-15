from app import db
from .repo import actions_ordered_by_date
from .book import Book, Copies
from . import bookaction
from flask import request, abort, jsonify
from sqlalchemy.exc import SQLAlchemyError
from app.catalog.service import does_book_exist
from app.receiver.service import does_receiver_exist


@bookaction.errorhandler(AssertionError)
@bookaction.errorhandler(ValueError)
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
    if not does_book_exist(book_id):
        abort(404, 'Taka książka nie istnieje w katalogu')

    data = request.get_json()
    book = Book(actions_ordered_by_date(book_id), book_id=book_id)
    action = book.receive(Copies(data.get('copies')))
    action.save()

    return jsonify({'message': '', 'status': 201}), 201


@bookaction.route('/release/<int:book_id>', methods=['POST'])
def release(book_id):
    if not does_book_exist(book_id):
        abort(404, 'Taka książka nie istnieje w katalogu')

    data = request.get_json()

    receiver_id = data.get('receiver') and int(data.get('receiver'))
    if not(receiver_id and does_receiver_exist(receiver_id)):
        abort(404, 'Taki użytkownik nie istnieje')

    book = Book(actions_ordered_by_date(book_id), book_id=book_id)
    action = book.release(
        Copies(data.get('copies')),
        receiver_id=receiver_id,
        comment=data.get('comment')
    )
    action.save()

    return jsonify({'message': '', 'status': 201}), 201
