from flask import request
from sqlalchemy import and_
from apps.auth.auth import Auth
from ..lib import response_json
from ..serialization.econom import Wallet, Income, Expense, Action
from apps.auth import decorators
from apps.econom import utils, models
from .. import decorators as api_decorators
from .. import lib
from .. import exceptions
from .. import actions


def init_econom(app):
    @app.route('/econom/wallet')
    @decorators.login_required_api
    @api_decorators.exception
    def wallet():
        user = Auth.get_user()
        wallet_list = models.Wallet.query.filter_by(user_id=user.id).all()
        data = {w.id: Wallet(id=w.id, title=w.title, balance=w.balance).dict() for w in wallet_list}

        return response_json(data=data)

    @app.route('/econom/wallet/edit', methods=['POST'])
    @decorators.login_required_api
    @api_decorators.exception
    def wallet_edit():
        user = Auth.get_user()
        json = request.get_json()
        action = json.get('action')
        title = json.get('title')
        balance = json.get('balance')

        if action == actions.wallet.ADD:
            models.Wallet.create(user, title)

        if action == actions.wallet.EDIT:
            w = models.Wallet.query.get(int(json.get('id')))
            if w:
                w.edit(title, balance)

        if action == actions.wallet.REMOVE:
            w = models.Wallet.query.get(int(json.get('id')))
            if w:
                w.remove()

        return response_json(data={})

    @app.route('/econom/income', methods=['GET'])
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

    @app.route('/econom/income', methods=['POST'])
    @decorators.login_required_api
    @api_decorators.exception
    def income_edit():
        user = Auth.get_user()
        action = request.args.get('action')
        json = request.get_json()

        if json is None:
            raise exceptions.NotHaveJson("NotHaveJson")
        json = Action.parse_raw(json)

        id = json.id
        title = json.title
        money = json.money
        wallet_id = json.wallet_id
        time_event = json.time_event

        if action is None:
            raise exceptions.NotHaveAction("NotHaveAction")

        if action == actions.income.ADD:
            income = models.Income.add(
                title=title,
                money=money,
                wallet=models.Wallet.query.filter_by(id=wallet_id, user_id=user.id).first(),
                time_event=time_event
            )
            if income:
                data = {
                    income.id: Income(
                        id=income.id, title=income.title, money=income.money,
                        wallet_id=income.wallet_id, time_event=income.time_event
                    ).dict()
                }

        if action == actions.income.REMOVE:
            income = models.Income.query.filter_by(id=id).first()
            if income.wallet.user_id != user.id:
                raise Exception('Income not found')
            if income is None:
                raise Exception('Income not found')
            income.delete()
            data = {'id': id}

        return response_json(data=data)

    @app.route('/econom/expense', methods=['GET'])
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

    @app.route('/econom/expense', methods=['POST'])
    @decorators.login_required_api
    @api_decorators.exception
    def expense_edit():
        user = Auth.get_user()
        action = request.args.get('action')
        json = request.get_json()

        if json is None:
            raise exceptions.NotHaveJson("NotHaveJson")
        json = Action.parse_raw(json)

        id = json.id
        title = json.title
        money = json.money
        wallet_id = json.wallet_id
        time_event = json.time_event

        if action is None:
            raise exceptions.NotHaveAction("NotHaveAction")

        wallet = None
        if wallet_id:
            wallet = models.Wallet.query.filter_by(id=wallet_id, user_id=user.id).first()

        if action == actions.expense.ADD:
            expense = models.Expense.add(
                title=title,
                money=money,
                wallet=wallet,
                time_event=time_event
            )
            if expense:
                data = {
                    expense.id: Expense(
                        id=expense.id, title=expense.title, money=expense.money,
                        wallet_id=expense.wallet_id, time_event=expense.time_event
                    ).dict()
                }

        if action == actions.expense.REMOVE:
            expense = models.Expense.query.filter_by(id=id).first()
            if expense.wallet.user_id != user.id:
                raise Exception('Expense not found')
            if expense is None:
                raise Exception('Expense not found')
            expense.delete()
            data = {'id': id}

        if action == actions.expense.EDIT:
            expense = models.Expense.query.filter_by(id=id).first()
            if expense.wallet.user_id != user.id:
                raise Exception('Expense not found')
            if expense is None:
                raise Exception('Expense not found')

            expense.edit(
                title=title,
                money=money,
                wallet=wallet,
                time_event=time_event
            )
            data = {
                expense.id: Expense(
                    id=expense.id, title=expense.title, money=expense.money,
                    wallet_id=expense.wallet_id, time_event=expense.time_event
                ).dict()
            }

        return response_json(data=data)
