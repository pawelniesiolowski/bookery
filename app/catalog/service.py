from .repo import book_by_id


def does_book_exist(book_id):
    return book_by_id(book_id) is not None
