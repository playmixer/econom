from core.database import db
import datetime
from apps.auth.models import User
from sqlalchemy import and_
from calendar import monthrange
import decimal


class Wallet(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    balance = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User, backref='wallets')

    @classmethod
    def create(cls, user: User, title):
        wallet = cls(title=title, user_id=user.id)
        db.session.add(wallet)
        db.session.commit()
        return wallet

    def remove(self):
        db.session.delete(self)
        db.session.commit()


class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    money = db.Column(db.Numeric(10, 2), nullable=False)
    wallet_id = db.Column(db.Integer, db.ForeignKey(Wallet.id))
    wallet = db.relationship(Wallet, backref='incomes')
    time_event = db.Column(db.DATETIME, nullable=False, default=datetime.datetime.now)
    time_created = db.Column(db.DATETIME, nullable=False, default=datetime.datetime.now)
    time_updated = db.Column(db.DATETIME, onupdate=datetime.datetime.now)

    @classmethod
    def add(cls, *, title, money, wallet, time_event):
        income = cls(
            title=title,
            money=money,
            wallet_id=wallet.id,
            time_event=time_event
        )

        wallet.balance += decimal.Decimal(money)

        db.session.add(income)
        db.session.commit()
        return income

    @classmethod
    def get_by_user(cls, user):
        wallet_list = Wallet.query.filter_by(user_id=user.id)
        incomes = Income.query.filter(cls.wallet_id.in_(list(wallet.id for wallet in wallet_list)))

        return incomes

    def delete(self):
        self.wallet.balance -= self.money
        db.session.delete(self)
        db.session.commit()


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    money = db.Column(db.Numeric(10, 2), nullable=False)
    wallet_id = db.Column(db.Integer, db.ForeignKey(Wallet.id))
    wallet = db.relationship(Wallet, backref='expenses')
    time_event = db.Column(db.DATETIME, nullable=False, default=datetime.datetime.now)
    time_created = db.Column(db.DATETIME, nullable=False, default=datetime.datetime.now)
    time_updated = db.Column(db.DATETIME, onupdate=datetime.datetime.now)

    @classmethod
    def add(cls, *, title, money, wallet, time_event):
        expense = cls(
            title=title,
            money=money,
            wallet_id=wallet.id,
            time_event=time_event
        )
        print(wallet.balance, decimal.Decimal(money))
        wallet.balance -= decimal.Decimal(money)

        db.session.add(expense)
        db.session.commit()
        return expense

    @classmethod
    def get_by_user(cls, user):
        wallet_list = Wallet.query.filter_by(user_id=user.id)
        expenses = Expense.query.filter(cls.wallet_id.in_(list(wallet.id for wallet in wallet_list)))

        return expenses

    def delete(self):
        self.wallet.balance += self.money
        db.session.delete(self)
        db.session.commit()


class WalletBar(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey(Wallet.id))
    wallet = db.relationship(Wallet, backref='bar')
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User, backref='wallet_bar')
