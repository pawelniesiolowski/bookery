from .book_model import Book


class BookRepo:
    def get_all_ordered_by_title(self):
        return Book.query.filter(
            Book.deleted_at.is_(None)
        ).order_by(
            Book.title.asc()
        ).all()

    def get_by_id(self, book_id):
        return Book.query.get(book_id)

    def does_title_exist(self, title):
        return Book.query.filter(Book.title == title).count() > 0
