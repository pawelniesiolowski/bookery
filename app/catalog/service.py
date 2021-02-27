from .repo import book_by_id, books_ordered_by_title


def does_book_exist(book_id):
    return book_by_id(book_id) is not None


def get_all_books():
    books = books_ordered_by_title()
    return [book.to_basic_data() for book in books]
