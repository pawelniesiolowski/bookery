"""Interface for accessing Catalog's data from external modules"""


from typing import List, Dict
from . import repo


def does_book_exist(book_id: int) -> bool:
    return repo.book_by_id(book_id) is not None


def get_all_books() -> List[Dict]:
    books = repo.all_existing(repo.BooksSorting('title', 'asc'))
    return [book.to_basic_data() for book in books]
