from flask import (
    request, render_template, redirect,
    url_for, flash, abort, current_app, jsonify
)
from sqlalchemy.exc import SQLAlchemyError
from . import catalog
from .. import db
from datetime import datetime
from .forms import BookForm
from .book_model import Book
from .book_repo import BookRepo
from app.bookaction.services import BookActionService


@catalog.route('/')
def index():
    try:
        books = BookRepo().get_all_ordered_by_title()
    except SQLAlchemyError as e:
        current_app.logger.error(e)
        abort(500)

    return render_template('catalog/index.html', books=books)


@catalog.route('/books/<int:book_id>')
def one(book_id):
    try:
        book = BookRepo().get_by_id(book_id)
    except SQLAlchemyError as e:
        current_app.logger.error(e)
        abort(500)

    if book is None:
        abort(404)

    book_action_service = BookActionService()
    copies = book_action_service.get_copies_for_book(book_id)

    return render_template('catalog/book.html', book=book, copies=copies)


@catalog.route('/books/form', methods=['GET', 'POST'])
def create():
    form = BookForm(request.form)
    if form.validate_on_submit():
        book = Book(
            form.title.data,
            authors=form.authors.data,
            isbn=form.isbn.data,
            price=form.price.data
        )
        try:
            book.save()
        except SQLAlchemyError as e:
            current_app.logger.error(e)
            db.session.rollback()
            abort(500)

        flash(f'Dodano książkę: {book.title}')
        return redirect(url_for('catalog.index'))

    return render_template(
        'catalog/form.html',
        form=form,
        subtitle='Dodaj książkę'
    )


@catalog.route('/books/<int:book_id>/form', methods=['GET', 'POST'])
def edit(book_id):
    try:
        book = BookRepo().get_by_id(book_id)
    except SQLAlchemyError as e:
        current_app.logger.error(e)
        abort(500)

    if book is None:
        return '', 404

    form = BookForm(request.form) if request.form else BookForm(obj=book)

    if form.validate_on_submit():
        form.populate_obj(book)
        try:
            book.save()
        except SQLAlchemyError as e:
            current_app.logger.error(e)
            db.session.rollback()
            abort(500)

        flash(f'Zmieniono dane książki: {book.title}')
        return redirect(url_for('catalog.index'))

    return render_template(
        'catalog/form.html',
        form=form,
        subtitle=f'Edytuj książkę: {book.title}'
    )


@catalog.route('/books/<int:book_id>', methods=['DELETE'])
def delete(book_id):
    try:
        book = BookRepo().get_by_id(book_id)
    except SQLAlchemyError as e:
        current_app.logger.error(e)
        abort(500)

    if book is None:
        return '', 404

    book.delete()

    try:
        book.save()
    except SQLAlchemyError as e:
        current_app.logger.error(e)
        db.session.rollback()
        abort(500)

    flash(f'Usunięto książkę: {book.title}')
    return '', 204


@catalog.route('/books/<string:title>/exists')
def exists(title):
    try:
        exists = BookRepo().does_title_exist(title)
    except SQLAlchemyError as e:
        current_app.logger.error(e)
        abort(500)

    return jsonify({'data': exists}), 200
