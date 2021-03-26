"""Test ISBN validator"""


from app.catalog import isbn_validator


def test_isbn_regex_matches_valid_isbn_examples():
    isbn_examples = [
        '979-83-283-0234-1',
        '9798328302341',
        '83-08-01120-9',
        '8308011209'
    ]
    for isbn in isbn_examples:
        assert isbn_validator.is_valid(isbn)


def test_isbn_regex_does_not_match_invalid_isbn_examples():
    isbn_examples = [
        '979-83-283-0234',
        '979832830234',
        '83-08-01120-91',
        '83080112091'
    ]
    for isbn in isbn_examples:
        assert not isbn_validator.is_valid(isbn)
