"""Controllers"""


from enum import Enum
from decimal import Decimal
from typing import Union, Tuple
from flask import (
    request, render_template, redirect,
    url_for, flash, abort, current_app, jsonify
    )
from flask_login import login_required
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.wrappers import Response
from app.bookaction import service as book_action
from .. import db
from . import catalog
from .forms import BookForm, ImageForm
from .models import Book, BookView
from . import repo
from .image_processor import ImageProcessor


@catalog.route('/')
@login_required
def index() -> Union[str, Response]:
    sorting = request.args.get('sorting', SortingFields.TITLE.value)

    try:
        books = []
        if sorting == SortingFields.INSERTED_AT.value:
            books = repo.books_ordered_by_date()
        elif sorting == SortingFields.AUTHORS.value:
            books = repo.books_ordered_by_authors()
        elif sorting == SortingFields.PUBLICATION_YEAR.value:
            books = repo.books_ordered_by_publication_year()
        else:
            books = repo.books_ordered_by_title()

        ids = [book.id for book in books]
        copies_for_ids = book_action.copies_for_books(ids)
    except SQLAlchemyError as ex:
        current_app.logger.error(ex)
        abort(500)

    books_views = []
    for book in books:
        books_views.append(BookView(book, copies_for_ids[book.id]))

    if sorting == SortingFields.COPIES.value:
        books_views.sort(reverse=True, key=lambda book_view: book_view.copies)

    if sorting == SortingFields.PRICE.value:
        books_views.sort(
            reverse=True,
            key=lambda book_view: book_view.price or Decimal()
            )

    return render_template(
        'catalog/index.html',
        books=books_views,
        sorting=sorting
        )


class SortingFields(Enum):
    TITLE = 'title'
    INSERTED_AT = 'inserted_at'
    AUTHORS = 'authors'
    PUBLICATION_YEAR = 'publication_year'
    PRICE = 'price'
    COPIES = 'copies'


@catalog.route('/books/<int:book_id>')
@login_required
def one(book_id: int) -> Union[str, Response]:
    try:
        book = repo.book_by_id(book_id)
    except SQLAlchemyError as ex:
        current_app.logger.error(ex)
        abort(500)

    if book is None:
        abort(404)

    copies = book_action.copies_for_book(book_id)
    actions = book_action.actions_for_book(book_id)

    image_processor = ImageProcessor(current_app.config['IMAGES_READ_DIR'])
    image_path = image_processor.create_path(book.image_name)

    return render_template(
        'catalog/book.html',
        book=book,
        image_path=image_path,
        copies=copies,
        actions=actions
        )


@catalog.route('/books/form', methods=['GET', 'POST'])
@login_required
def create() -> Union[str, Response]:
    form = BookForm(request.form)
    if form.validate_on_submit():
        book = Book(
            form.title.data,
            authors=form.authors.data,
            isbn=form.isbn.data,
            price=form.price.data,
            publication_year=form.publication_year.data
            )
        try:
            book.save()
        except SQLAlchemyError as ex:
            current_app.logger.error(ex)
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
def edit(book_id: int) -> Union[str, Response, Tuple[str, int]]:
    try:
        book = repo.book_by_id(book_id)
    except SQLAlchemyError as ex:
        current_app.logger.error(ex)
        abort(500)

    if book is None:
        return '', 404

    form = BookForm(request.form) if request.form else BookForm(obj=book)

    if form.validate_on_submit():
        form.populate_obj(book)
        try:
            book.save()
        except SQLAlchemyError as ex:
            current_app.logger.error(ex)
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
def delete(book_id: int) -> Union[Tuple[str, int], Response]:
    try:
        book = repo.book_by_id(book_id)
    except SQLAlchemyError as ex:
        current_app.logger.error(ex)
        abort(500)

    if book is None:
        return '', 404

    book.delete()

    try:
        book.save()
    except SQLAlchemyError as ex:
        current_app.logger.error(ex)
        db.session.rollback()
        abort(500)

    flash(f'Usunięto książkę: {book.title}')
    return '', 204


@catalog.route('/books/<string:title>/exists')
@login_required
def check_existing(title: str) -> Union[Tuple[str, int], Response]:
    try:
        exists = repo.does_title_exist(title)
    except SQLAlchemyError as ex:
        current_app.logger.error(ex)
        abort(500)

    return jsonify({'data': exists}), 200


@catalog.route('/books/<int:book_id>/image', methods=['GET', 'POST'])
@login_required
def upload_image(book_id: int) -> Union[str, Response]:
    form = ImageForm()
    if form.validate_on_submit():
        try:
            book = repo.book_by_id(book_id)
        except SQLAlchemyError as ex:
            current_app.logger.error(ex)
            abort(500)

        if book is None:
            abort(404)

        image_processor = ImageProcessor(
                current_app.config['IMAGES_WRITE_DIR']
                )

        new_image_name = image_processor.process(form.image.data)
        previous_image_name = book.image_name
        book.image_name = new_image_name

        try:
            book.save()
        except SQLAlchemyError as ex:
            current_app.logger.error(ex)
            db.session.rollback()
            image_processor.remove(new_image_name)
            abort(500)

        if previous_image_name:
            try:
                image_processor.remove(previous_image_name)
            except OSError as ex:
                current_app.logger.error(ex)

        return redirect(url_for('catalog.one', book_id=book_id))

    return render_template(
        'catalog/image_form.html',
        form=form
        )
