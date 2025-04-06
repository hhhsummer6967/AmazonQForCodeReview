import abc
from typing import Any

from ewallet.repository.base_repository import BaseRepository
from ewallet.model.wallet import Wallet
from ewallet.model.transaction import Transaction

class TransactionRepository(BaseRepository):
  """
  Abstract class that extends `repository.Repository`
  and adds specific methods for interacting with `Transaction` objects.
  """
  @abc.abstractmethod
  def list_transactions_by_wallet(self, wallet: Wallet) -> list[Transaction]:
    """
    Returns a list of transactions for a given wallet.

    :param str wallet: The wallet to retrieve transactions for.
    :return: A list of transactions for the given wallet.
    :rtype: list[Any]
    """
    pass
