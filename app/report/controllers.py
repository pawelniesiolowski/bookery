"""Controllers"""


import io
from flask import send_file, current_app, abort
from flask_login import login_required
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.wrappers import Response
import app.catalog.service as catalog
import app.bookaction.service as book_action
from . import report as report_module
from .xml_report import XmlBooksReport


@report_module.route('/report')
@login_required
def show() -> Response:
    try:
        books = catalog.get_all_books()
        for book in books:
            copies = book_action.copies_for_book(book['id'])
            book['copies'] = copies

    except SQLAlchemyError as ex:
        current_app.logger.error(ex)
        abort(500)

    report = XmlBooksReport()
    report.prepare(books)
    out = io.BytesIO()
    report.save(out)
    out.seek(0)

    mimetype = (
        'application/'
        'vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

    return send_file(
        out,
        mimetype=mimetype,
        attachment_filename='report.xlsx',
        as_attachment=True
        )
