"""Repository"""


from enum import Enum
from typing import List, Optional
from sqlalchemy.sql.elements import UnaryExpression
from .models import Book


class DbSortingFields(Enum):
    TITLE = 'title'
    INSERTED_AT = 'inserted_at'
    AUTHORS = 'authors'
    PUBLICATION_YEAR = 'publication_year'


class DbSortingTypes(Enum):
    ASC = 'asc'
    DESC = 'desc'


class BooksSorting:
    DEFAULT_SORTING_FIELD = DbSortingFields.TITLE.value
    DEFAULT_SORTING_TYPE = DbSortingTypes.ASC.value
    FIELDS = [sorting_field.value for sorting_field in DbSortingFields]
    TYPES = [sorting_type.value for sorting_type in DbSortingTypes]

    def __init__(self, sorting_field: str, sorting_type: str):
        if (
            sorting_field not in BooksSorting.FIELDS
            or sorting_type not in BooksSorting.TYPES
        ):
            sorting_field = BooksSorting.DEFAULT_SORTING_FIELD
            sorting_type = BooksSorting.DEFAULT_SORTING_TYPE

        self._sorting_field = sorting_field
        self._sorting_type = sorting_type

    def to_query(self) -> UnaryExpression:
        field = getattr(Book, self._sorting_field)
        return getattr(field, self._sorting_type)()


def all_existing(sorting: BooksSorting) -> List[Book]:
    return Book.query.filter(
        Book.deleted_at.is_(None)
        ).order_by(
        sorting.to_query()
        ).all()


def book_by_id(book_id: int) -> Optional[Book]:
    return Book.query.get(book_id)


def does_title_exist(title: str) -> bool:
    return Book.query.filter(Book.title == title).count() > 0
