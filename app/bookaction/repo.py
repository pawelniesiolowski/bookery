"""Repository"""


from typing import List
from .models import BookAction


def actions_ordered_by_date_asc(book_id: int) -> List[BookAction]:
    return BookAction.query.filter(
        BookAction.book_id == book_id
        ).order_by(
        BookAction.inserted_at.asc()
        ).all()


def actions_ordered_by_date_desc(book_id: int) -> List[BookAction]:
    return BookAction.query.filter(
        BookAction.book_id == book_id
        ).order_by(
        BookAction.inserted_at.desc()
        ).all()


def all_actions_ordered_by_date_desc() -> List[BookAction]:
    return BookAction.query.order_by(BookAction.inserted_at.desc()).all()
