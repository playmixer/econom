from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from apps.auth import decorators
from . import forms
from .models import *
from apps.auth.auth import Auth
from . import utils

econom_app = Blueprint(
    'econom',
    __name__,
    template_folder='templates'
)


@econom_app.context_processor
def add_processor():
    return dict(
        utils=utils
    )


@econom_app.route('/')
@decorators.login_required
def index():
    return redirect(url_for('.wallets'))
    # return render_template('econom/econom.html')


@econom_app.route('/wallet')
@decorators.login_required
def wallets():
    wallet_list = Wallet.query.filter_by(user_id=Auth.get_user().id)

    return render_template('econom/wallet/wallets.html', wallet_list=wallet_list)


@econom_app.route('/wallet/create', methods=['GET', 'POST'])
@decorators.login_required
def wallet_create():
    form = forms.Wallet()
    if form.is_submitted():
        title = request.form.get('title')

    if form.validate_on_submit():
        user = Auth.get_user()
        wallet = Wallet.create(
            user=user,
            title=title
        )

        if wallet:
            return redirect(url_for('econom.wallet_edit', wallet_id=wallet.id))

    return render_template('econom/wallet/create.html', form=form)


# @econom_app.route('/wallet/<wallet_id>', methods=['GET', 'POST'])
# @decorators.login_required
# def wallet(wallet_id):
#     user = Auth.get_user()
#     wallet = Wallet.query.filter_by(id=wallet_id, user_id=user.id).first()
#     if not wallet:
#         return abort(404)
#
#     form = forms.Wallet()
#     if form.validate_on_submit():
#         title = request.form.get('title')
#         balance = request.form.get('balance')
#         wallet.title = title
#         wallet.balance = balance
#         db.session.commit()
#         flash('Изменения сохранены')
#         return redirect(request.url)
#
#     return render_template('econom/wallet/wallet.html', form=form, wallet=wallet)


@econom_app.route('/wallet/<wallet_id>/edit', methods=['GET', 'POST'])
@decorators.login_required
def wallet_edit(wallet_id):
    user = Auth.get_user()
    wallet = Wallet.query.filter_by(id=wallet_id, user_id=user.id).first()
    if not wallet:
        return abort(404)

    form = forms.Wallet()
    if form.validate_on_submit():
        title = request.form.get('title')
        balance = request.form.get('balance')
        wallet.title = title
        wallet.balance = balance
        db.session.commit()
        flash('Изменения сохранены')
        return redirect(request.url)

    return render_template('econom/wallet/edit.html', form=form, wallet=wallet)


@econom_app.route('/wallet/<wallet_id>/delete', methods=['GET', 'POST'])
@decorators.login_required
def wallet_delete(wallet_id):
    user = Auth.get_user()
    wallet = Wallet.query.filter_by(id=wallet_id, user_id=user.id).first()
    if not wallet:
        return abort(404)

    form = forms.Yes()
    if form.validate_on_submit():
        wallet.remove()
        return redirect(url_for('.wallets'))

    return render_template('econom/wallet/delete.html', form=form, wallet=wallet)


@econom_app.route('/finance')
@decorators.login_required
def finance():
    return redirect(url_for('.expense'))
    return render_template('econom/expense/expense.html')


@econom_app.route('/expense')
@decorators.login_required
def expense():
    user = Auth.get_user()

    month, year = utils.selected_month()
    d1, d2 = utils.max_min_datetime_in_month(month, year)

    expense_list = Expense.get_by_user(user).filter(and_(Expense.time_event >= d1, Expense.time_event <= d2))

    return render_template('econom/expense/expense.html', expense_list=expense_list, month=month, year=year)


@econom_app.route('/expense/add', methods=['GET', 'POST'])
@decorators.login_required
def expense_add():
    user = Auth.get_user()
    form = forms.Expense()
    form.wallet_id.choices = list((wallet.id, wallet.title)
                                  for wallet in Wallet.query.filter_by(user_id=user.id).all())

    if form.is_submitted():
        title = request.form.get('title')
        money = request.form.get('money')
        wallet_id = request.form.get('wallet_id')
        time_event = request.form.get('time_event')

    if form.validate_on_submit():
        wallet = Wallet.query.get(wallet_id)
        Expense.add(
            title=title,
            money=money,
            wallet=wallet,
            time_event=time_event
        )
        return redirect(url_for('.expense'))

    return render_template('econom/expense/add.html', form=form)


@econom_app.route('/expense/<expense_id>/delete', methods=['GET', 'POST'])
@decorators.login_required
def expense_delete(expense_id):
    expense = Expense.query.get(expense_id)

    form = forms.Yes()
    if form.validate_on_submit():
        expense.delete()
        return redirect(url_for('.expense'))

    return render_template('econom/expense/delete.html', form=form, expense=expense)


@econom_app.route('/income')
@decorators.login_required
def income():
    user = Auth.get_user()

    month, year = utils.selected_month()
    d1, d2 = utils.max_min_datetime_in_month(month, year)

    income_list = Income.get_by_user(user).filter(and_(Expense.time_event >= d1, Expense.time_event <= d2))

    return render_template('econom/income/income.html', income_list=income_list, month=month, year=year)


@econom_app.route('/income/add', methods=['GET', 'POST'])
@decorators.login_required
def income_add():
    user = Auth.get_user()
    form = forms.Income()
    form.wallet_id.choices = list((wallet.id, wallet.title)
                                  for wallet in Wallet.query.filter_by(user_id=user.id).all())

    if form.is_submitted():
        title = request.form.get('title')
        money = request.form.get('money')
        wallet_id = request.form.get('wallet_id')
        time_event = request.form.get('time_event')

    if form.validate_on_submit():
        wallet = Wallet.query.get(wallet_id)
        Income.add(
            title=title,
            money=money,
            wallet=wallet,
            time_event=time_event
        )
        return redirect(url_for('.income'))
    return render_template('econom/income/add.html', form=form)


@econom_app.route('/income/<income_id>/delete', methods=['GET', 'POST'])
@decorators.login_required
def income_delete(income_id):
    income = Income.query.get(income_id)

    form = forms.Yes()
    if form.validate_on_submit():
        income.delete()
        return redirect(url_for('.income'))

    return render_template('econom/income/delete.html', form=form, income=income)
