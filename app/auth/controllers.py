from . import auth
from flask import (
    render_template, request, redirect, url_for, flash, jsonify, current_app
)
from .forms import UserForm
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .recaptcha import verify


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = UserForm(request.form)
    captcha_key = current_app.config['CAPTCHA_PUBLIC_KEY']

    if form.validate_on_submit():
        recaptcha_response = request.form.get('g-recaptcha-response')

        if not verify(recaptcha_response):
            flash('Błąd recaptchy')
            return redirect(url_for('auth.login'))

        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            user_ip = request.headers.get('X-Real-IP', request.remote_addr)
            current_app.logger.warning(
                f'Nieprawidłowe dane logowania.'
                f'Email: {email}, ip: {user_ip}.'
            )
            flash('Podano nieprawidłowe dane logowania')
            return redirect(url_for('auth.login'))

        login_user(user)
        return redirect(url_for('catalog.index'))

    return render_template(
        'auth/login.html',
        form=form,
        captcha_key=captcha_key
    )


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('catalog.index'))


@auth.route('/hash/<string:password>')
def hash(password):
    return generate_password_hash(password, method='sha256')
