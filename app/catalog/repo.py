from .models import Book


def books_ordered_by_title():
    return Book.query.filter(
        Book.deleted_at.is_(None)
    ).order_by(
        Book.title.asc()
    ).all()


def book_by_id(book_id):
    return Book.query.get(book_id)


def does_title_exist(title):
    return Book.query.filter(Book.title == title).count() > 0
