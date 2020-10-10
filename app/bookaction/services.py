from .book_action_model import BookAction
from .book import Book


class BookActionService:
    def get_copies_for_book(self, book_id):
        actions = BookAction.query.filter(BookAction.book_id == book_id).all()
        book = Book(actions)
        return book.copies
