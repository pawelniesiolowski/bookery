"""Repository"""


from typing import List
from datetime import datetime
from .models import BookAction


def actions_ordered_by_date_asc(book_id: int) -> List[BookAction]:
    return BookAction.query.filter(
        BookAction.book_id == book_id
        ).order_by(
        BookAction.inserted_at.asc()
        ).all()


def actions_before_date_ordered_by_date_asc(
        book_id: int,
        before_date: datetime
        ) -> List[BookAction]:
    return BookAction.query.filter(
        BookAction.book_id == book_id,
        BookAction.inserted_at <= before_date
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
