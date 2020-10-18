from flask import (
    request, render_template, redirect,
    url_for, flash, abort, current_app, jsonify
)
from sqlalchemy.exc import SQLAlchemyError
from . import catalog
from .. import db
from datetime import datetime
from .forms import BookForm
from .models import Book
from .repo import books_ordered_by_title, book_by_id, does_title_exist
from app.bookaction.service import copies_for_book, actions_for_book
from flask_login import login_required


@catalog.route('/')
def index():
    try:
        books = books_ordered_by_title()
    except SQLAlchemyError as e:
        current_app.logger.error(e)
        abort(500)

    return render_template('catalog/index.html', books=books)


@catalog.route('/books/<int:book_id>')
@login_required
def one(book_id):
    try:
        book = book_by_id(book_id)
    except SQLAlchemyError as e:
        current_app.logger.error(e)
        abort(500)

    if book is None:
        abort(404)

    copies = copies_for_book(book_id)
    actions = actions_for_book(book_id)

    return render_template(
        'catalog/book.html',
        book=book,
        copies=copies,
        actions=actions
    )


@catalog.route('/books/form', methods=['GET', 'POST'])
@login_required
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
@login_required
def edit(book_id):
    try:
        book = book_by_id(book_id)
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
@login_required
def delete(book_id):
    try:
        book = book_by_id(book_id)
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
@login_required
def exists(title):
    try:
        exists = does_title_exist(title)
    except SQLAlchemyError as e:
        current_app.logger.error(e)
        abort(500)

    return jsonify({'data': exists}), 200
