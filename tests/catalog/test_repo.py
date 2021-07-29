"""Test repo in catalog"""


from app.catalog.repo import BooksSorting


def test_it_creates_sorting_query():
    books_sorting = BooksSorting('publication_year', 'desc')
    assert str(books_sorting.to_query()) == 'book.publication_year DESC'


def test_it_uses_default_values():
    books_sorting = BooksSorting('invalid', 'invalid')
    assert str(books_sorting.to_query()) == 'book.title ASC'
