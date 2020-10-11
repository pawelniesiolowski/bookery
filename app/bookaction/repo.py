from .models import BookAction


def actions_ordered_by_date(book_id):
    return BookAction.query.filter(
        BookAction.book_id == book_id
    ).order_by(
        BookAction.inserted_at.asc()
    ).all()
