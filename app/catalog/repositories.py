from .models import Book


class BookRepo:
    def getAllOrderedByTitle(self):
        return Book.query.filter(
            Book.deleted_at.is_(None)
        ).order_by(
            Book.title.asc()
        ).all()

    def getById(self, book_id):
        return Book.query.get(book_id)
