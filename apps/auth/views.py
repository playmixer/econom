from flask import Blueprint, render_template, request, redirect, url_for, flash
from .forms import *
from .auth import Auth
from . import decorators
from apps.econom.models import WalletBar

__all__ = ['auth_app']

auth_app = Blueprint(
    'auth',
    __name__,
    template_folder='templates'
)


@auth_app.route('/login', methods=['POST', 'GET'])
def login():
    form = FormLogin()
    if form.is_submitted():
        username = request.form.get('username')
        password = request.form.get('password')

    if form.validate_on_submit():
        auth = Auth()
        auth.login(username, password)
        if not auth.is_authenticated():
            flash('Не верный логин или пароль', 'error')
            return render_template('auth/login.html', form=form, error='error')
        return redirect(url_for('econom.index'))
    return render_template('auth/login.html', form=form)


@auth_app.route('/logout', methods=['POST', 'GET'])
def logout():
    auth = Auth()
    auth.logout()
    return redirect(url_for('auth.login'))


@auth_app.route('/cabinet', methods=['GET'])
@decorators.login_required
def cabinet():
    return render_template('auth/cabinet.html')


@auth_app.route('/cabinet/balance-bar', methods=['GET'])
@decorators.login_required
def balance_bar():
    user = Auth.get_user()
    wallets = user.wallets
    wallet_bar = user.wallet_bar
    w_choices = list((w.id, w.title) for w in wallets)
    print(w_choices)
    form = BalanceBar()
    form.wallets.choices = w_choices
    if form.validate_on_submit():
        ...
    return render_template('auth/balance_bar.html', form=form)
