from apps.econom.models import Wallet


def transfer_cash(wallet_from, cash_from, wallet_to, cash_to):
    if wallet_from == wallet_to:
        wallet_from.cash += cash_from
        wallet_from.cash -= cash_to
        wallet_from.save()
    else:
        wallet_from.cash += cash_from
        wallet_from.save()
        wallet_to.cash -= cash_to
        wallet_to.save()
