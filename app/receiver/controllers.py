from flask import (
    request, render_template, redirect,
    url_for, flash, abort, current_app
)
from sqlalchemy.exc import SQLAlchemyError
from . import receiver
from .forms import ReceiverForm
from .receiver_model import Receiver
from .receiver_repo import ReceiverRepo


@receiver.route('/receivers')
def index():
    try:
        receivers = ReceiverRepo().get_all_ordered_by_surname()
    except SQLAlchemyError as e:
        current_app.logger.error(e)
        db.session.rollback()
        abort(500)

    return render_template('receiver/index.html', receivers=receivers)


@receiver.route('/receivers/form', methods=['GET', 'POST'])
def create():
    form = ReceiverForm(request.form)
    if form.validate_on_submit():
        receiver = Receiver(form.name.data, form.surname.data)
        if ReceiverRepo().does_receiver_exist(receiver):
            flash(
                f'Użytkownik: {receiver.name} {receiver.surname} już istnieje',
                'error'
            )
            return render_template(
                'receiver/form.html',
                form=form,
                subtitle='Dodaj użytkownika'
            )
        try:
            receiver.save()
        except SQLAlchemyError as e:
            current_app.logger.error(e)
            db.session.rollback()
            abort(500)

        flash(f'Dodano użytkownika: {receiver.name} {receiver.surname}')
        return redirect(url_for('receiver.index'))

    return render_template(
        'receiver/form.html',
        form=form,
        subtitle='Dodaj użytkownika'
    )


@receiver.route('/receivers/<int:receiver_id>/form', methods=['GET', 'POST'])
def edit(receiver_id):
    try:
        receiver = ReceiverRepo().get_by_id(receiver_id)
    except SQLAlchemyError as e:
        current_app.logger.error(e)
        db.session.rollback()
        abort(500)

    if receiver is None:
        return '', 404

    form = ReceiverForm(request.form) if request.form\
        else ReceiverForm(obj=receiver)

    if form.validate_on_submit():
        form.populate_obj(receiver)
        try:
            receiver.save()
        except SQLAlchemyError as e:
            current_app.logger.error(e)
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


@receiver.route('/receivers/<int:receiver_id>', methods=['DELETE'])
def delete(receiver_id):
    try:
        receiver = ReceiverRepo().get_by_id(receiver_id)
    except SQLAlchemyError as e:
        current_app.logger.error(e)
        db.session.rollback()
        abort(500)

    if receiver is None:
        return '', 404

    receiver.delete()

    try:
        receiver.save()
    except SQLAlchemyError as e:
        current_app.logger.error(e)
        db.session.rollback()
        abort(500)

    flash(f'Usunięto użytkownika: {receiver.name} {receiver.surname}')
    return '', 204
