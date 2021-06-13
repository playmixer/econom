from flask import request
from sqlalchemy import and_
from apps.auth.auth import Auth
from ..lib import response_json
from ..intefrace.econom import Wallet, Income, Expense
from apps.auth import decorators
from apps.econom import utils, models
from .. import decorators as api_decorators
from .. import lib


def init_econom(app):
    @app.route('/econom/wallet')
    @decorators.login_required_api
    @api_decorators.exception
    def wallet():
        user = Auth.get_user()
        wallet_list = models.Wallet.query.filter_by(user_id=user.id).all()
        data = {w.id: Wallet(id=w.id, title=w.title, balance=w.balance).dict() for w in wallet_list}

        return response_json(data=data)

    @app.route('/econom/income')
    @decorators.login_required_api
    @api_decorators.exception
    def income():
        user = Auth.get_user()

        year = lib.to_int(request.args.get('year'))
        month = lib.to_int(request.args.get('month'))

        if year is None or month is None:
            month, year = utils.selected_month()
        d1, d2 = utils.max_min_datetime_in_month(month, year)
        income_list = models.Income.get_by_user(user) \
            .filter(and_(models.Income.time_event >= d1, models.Income.time_event <= d2)) \
            .order_by(models.Income.time_event.desc()).all()

        data = {
            income.id: Income(
                id=income.id, title=income.title, money=income.money,
                wallet_id=income.wallet_id, time_event=income.time_event).dict()
            for income in income_list
        }

        return response_json(data=data)

    @app.route('/econom/expense')
    @decorators.login_required_api
    @api_decorators.exception
    def expense():
        user = Auth.get_user()

        year = lib.to_int(request.args.get('year'))
        month = lib.to_int(request.args.get('month'))

        if year is None or month is None:
            month, year = utils.selected_month()
        d1, d2 = utils.max_min_datetime_in_month(month, year)
        expense_list = models.Expense.get_by_user(user) \
            .filter(and_(models.Expense.time_event >= d1, models.Expense.time_event <= d2)) \
            .order_by(models.Expense.time_event.desc()).all()

        data = {
            expense.id: Expense(
                id=expense.id, title=expense.title, money=expense.money,
                wallet_id=expense.wallet_id, time_event=expense.time_event).dict()
            for expense in expense_list
        }

        return response_json(data=data)
