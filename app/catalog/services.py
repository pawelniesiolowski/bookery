from .book_repo import BookRepo


class BookService:
    def does_book_exist(self, book_id):
        return BookRepo().get_by_id(book_id) is not None
