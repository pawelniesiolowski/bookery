from . import auth
from flask import render_template, request, redirect, url_for, flash
from .forms import UserForm
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = UserForm(request.form)

    if form.validate_on_submit():
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash('Podano nieprawidłowe dane logowania')
            return redirect(url_for('auth.login'))

        login_user(user)
        return redirect(url_for('catalog.index'))

    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('catalog.index'))


@auth.route('/hash/<string:password>')
def hash(password):
    return generate_password_hash(password, method='sha256')
