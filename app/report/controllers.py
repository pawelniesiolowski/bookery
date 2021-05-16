"""Controllers"""


from typing import Union
import io
from datetime import datetime
from flask import send_file, current_app, abort, request, render_template
from flask_login import login_required
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.wrappers import Response
import app.catalog.service as catalog
import app.bookaction.service as book_action
from . import report as report_module
from .xml_report import XmlBooksReport
from .forms import ReportForm


@report_module.route('/report', methods=['GET', 'POST'])
@login_required
def show() -> Union[str, Response]:
    form = ReportForm(request.form)
    if form.validate_on_submit():
        try:
            books = catalog.get_all_books()
            books_with_actions = []

            date = form.date.data
            before_date = datetime(date.year, date.month, date.day, 23, 59, 59)

            for book in books:
                (actions, copies) = (
                        book_action.maybe_copies_for_book_before_date(
                            book['id'],
                            before_date
                            )
                        )
                book['copies'] = copies

                if actions:
                    books_with_actions.append(book)

        except SQLAlchemyError as ex:
            current_app.logger.error(ex)
            abort(500)

        report = XmlBooksReport()
        report.prepare(books_with_actions)
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

    return render_template(
        'report/form.html',
        form=form,
        subtitle='Wygeneruj raport'
        )
