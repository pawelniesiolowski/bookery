"""Controllers"""


from typing import Union, Tuple
from flask import (
    request, render_template, redirect,
    url_for, flash, abort, current_app, jsonify
    )
from flask_login import login_required
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.wrappers import Response
from .. import db
from . import receiver as receiver_module
from .forms import ReceiverForm
from .models import Receiver
from . import repo


@receiver_module.route('/receivers/index')
@login_required
def index() -> Union[str, Response]:
    try:
        receivers = repo.receivers_ordered_by_surname()
    except SQLAlchemyError as ex:
        current_app.logger.error(ex)
        abort(500)

    return render_template('receiver/index.html', receivers=receivers)


@receiver_module.route('/receivers/form', methods=['GET', 'POST'])
@login_required
def create() -> Union[str, Response]:
    form = ReceiverForm(request.form)
    if form.validate_on_submit():
        receiver = Receiver(form.name.data, form.surname.data)
        try:
            existing_receiver = repo.receiver_by_name(
                receiver.name,
                receiver.surname
                )
        except SQLAlchemyError as ex:
            current_app.logger.error(ex)
            abort(500)

        if existing_receiver and existing_receiver.deleted_at is None:
            flash(
                f'Użytkownik: {receiver.name} {receiver.surname} już istnieje',
                'error'
                )
            return render_template(
                'receiver/form.html',
                form=form,
                subtitle='Dodaj użytkownika'
                )
        if existing_receiver:
            receiver = existing_receiver
            receiver.deleted_at = None

        try:
            receiver.save()
        except SQLAlchemyError as ex:
            current_app.logger.error(ex)
            db.session.rollback()
            abort(500)

        flash(f'Dodano użytkownika: {receiver.name} {receiver.surname}')
        return redirect(url_for('receiver.index'))

    return render_template(
        'receiver/form.html',
        form=form,
        subtitle='Dodaj użytkownika'
        )


@receiver_module.route(
    '/receivers/<int:receiver_id>/form',
    methods=['GET', 'POST']
    )
@login_required
def edit(receiver_id: int) -> Union[str, Response, Tuple[str, int]]:
    try:
        receiver = repo.receiver_by_id(receiver_id)
    except SQLAlchemyError as ex:
        current_app.logger.error(ex)
        abort(500)

    if receiver is None:
        return '', 404

    form = ReceiverForm(request.form) if request.form\
        else ReceiverForm(obj=receiver)

    if form.validate_on_submit():
        form.populate_obj(receiver)
        try:
            receiver.save()
        except SQLAlchemyError as ex:
            current_app.logger.error(ex)
            db.session.rollback()
            abort(500)

        msg = f'Zmieniono dane użytkownika: {receiver.name} {receiver.surname}'
        flash(msg)
        return redirect(url_for('receiver.index'))

    return render_template(
        'receiver/form.html',
        form=form,
        subtitle=f'Edytuj dane użytkownika: {receiver.name} {receiver.surname}'
        )


@receiver_module.route('/receivers/<int:receiver_id>', methods=['DELETE'])
@login_required
def delete(receiver_id: int) -> Union[Tuple[str, int], Response]:
    try:
        receiver = repo.receiver_by_id(receiver_id)
    except SQLAlchemyError as ex:
        current_app.logger.error(ex)
        abort(500)

    if receiver is None:
        return '', 404

    receiver.delete()

    try:
        receiver.save()
    except SQLAlchemyError as ex:
        current_app.logger.error(ex)
        db.session.rollback()
        abort(500)

    flash(f'Usunięto użytkownika: {receiver.name} {receiver.surname}')
    return '', 204


@receiver_module.route('/receivers')
@login_required
def show_all() -> Union[Tuple[str, int], Response]:
    try:
        receivers = repo.receivers_ordered_by_surname()
    except SQLAlchemyError as ex:
        current_app.logger.error(ex)
        abort(500)

    data = [receiver.format() for receiver in receivers]
    return jsonify({
        'status': 200,
        'data': data
        }), 200
