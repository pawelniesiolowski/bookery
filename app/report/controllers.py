from flask import send_file
from sqlalchemy.exc import SQLAlchemyError
from . import report
from flask_login import login_required
from app.catalog.service import get_all_books
from app.bookaction.service import copies_for_book
from .xml_report import XmlBooksReport
import io

@report.route('/report')
@login_required
def show():
    try:
        books = get_all_books()
        for book in books:
            copies = copies_for_book(book['id'])
            book['copies'] = copies

    except SQLAlchemyError as e:
        current_app.logger.error(e)
        abort(500)

    report = XmlBooksReport()
    report.prepare(books)
    out = io.BytesIO()
    report.save(out)
    out.seek(0)

    return send_file(
        out,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        attachment_filename='report.xlsx',
        as_attachment=True
    )
