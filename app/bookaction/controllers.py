"""Controllers"""


from typing import Union, Tuple
from flask import request, abort, jsonify, current_app
from flask_login import login_required
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import NotFound, BadRequest, InternalServerError
from werkzeug.wrappers import Response
from app import db
from app.catalog import service as catalog
from app.receiver import service as receiver
from . import repo
from .book import Book, Copies
from . import bookaction


@bookaction.errorhandler(AssertionError)
@bookaction.errorhandler(ValueError)
@bookaction.errorhandler(400)
def validation_error(
        ex: Union[AssertionError, ValueError, BadRequest]
        ) -> Tuple[str, int]:
    error = {
        'error': str(ex),
        'status': 400
        }
    return jsonify(error), 400


@bookaction.errorhandler(SQLAlchemyError)
def database_error(_: SQLAlchemyError) -> Tuple[str, int]:
    db.session.rollback()
    return jsonify({
        'error': 'Internal server error',
        'status': 500
        }), 500


@bookaction.errorhandler(404)
def not_found(ex: NotFound) -> Tuple[str, int]:
    error = {
        'error': str(ex),
        'status': 404
        }
    return jsonify(error), 404


@bookaction.errorhandler(500)
def internal_server_error(ex: InternalServerError) -> Tuple[str, int]:
    error = {
        'error': str(ex),
        'status': 500
        }
    return jsonify(error), 500


@bookaction.route('/receive/<int:book_id>', methods=['POST'])
@login_required
def receive(book_id: int) -> Union[Tuple[str, int], Response]:
    if not catalog.does_book_exist(book_id):
        abort(404, 'Taka książka nie istnieje w katalogu')

    data = request.get_json()
    book = Book(repo.actions_ordered_by_date_asc(book_id), book_id=book_id)
    action = book.receive(Copies(int(data.get('copies'))))
    try:
        action.save()
    except SQLAlchemyError as ex:
        current_app.logger.error(ex)
        db.session.rollback()
        abort(500, 'Nie udało się zapisać akcji')

    return jsonify({'message': '', 'status': 201}), 201


@bookaction.route('/release/<int:book_id>', methods=['POST'])
@login_required
def release(book_id: int) -> Union[Tuple[str, int], Response]:
    if not catalog.does_book_exist(book_id):
        abort(404, 'Taka książka nie istnieje w katalogu')

    data = request.get_json()

    receiver_id = data.get('receiver') and int(data.get('receiver'))
    if not(receiver_id and receiver.does_receiver_exist(receiver_id)):
        abort(404, 'Taki użytkownik nie istnieje')

    book = Book(repo.actions_ordered_by_date_asc(book_id), book_id=book_id)
    action = book.release(
        Copies(int(data.get('copies'))),
        receiver_id=receiver_id,
        comment=data.get('comment')
        )

    try:
        action.save()
    except SQLAlchemyError as ex:
        current_app.logger.error(ex)
        db.session.rollback()
        abort(500, 'Nie udało się zapisać akcji')

    return jsonify({'message': '', 'status': 201}), 201


@bookaction.route('/sell/<int:book_id>', methods=['POST'])
@login_required
def sell(book_id: int) -> Union[Tuple[str, int], Response]:
    if not catalog.does_book_exist(book_id):
        abort(404, 'Taka książka nie istnieje w katalogu')

    data = request.get_json()

    book = Book(repo.actions_ordered_by_date_asc(book_id), book_id=book_id)
    action = book.sell(Copies(int(data.get('copies'))))

    try:
        action.save()
    except SQLAlchemyError as ex:
        current_app.logger.error(ex)
        db.session.rollback()
        abort(500, 'Nie udało się zapisać akcji')

    return jsonify({'message': '', 'status': 201}), 201


@bookaction.route(
    '/sell/<int:book_id>/<int:action_id>',
    methods=['POST']
    )
@login_required
def sell_released(
        book_id: int,
        action_id: int
        ) -> Union[Tuple[str, int], Response]:
    if not catalog.does_book_exist(book_id):
        abort(404, 'Taka książka nie istnieje w katalogu')

    data = request.get_json()

    book = Book(repo.actions_ordered_by_date_asc(book_id), book_id=book_id)
    try:
        action = book.sell_released(
            Copies(int(data.get('copies'))),
            release_id=action_id
            )
        action.save_in_transaction()
        db.session.commit()
    except (ValueError, AssertionError) as ex:
        current_app.logger.error(ex)
        db.session.rollback()
        msg = 'Liczba sprzedanych książek musi być mniejsza lub równa \
wydanym książkom oraz większa od zera'
        abort(400, msg)
    except SQLAlchemyError as ex:
        current_app.logger.error(ex)
        db.session.rollback()
        abort(500, 'Niestety nie udało się sprzedać wydanych książek')

    return jsonify({'message': '', 'status': 201}), 201
