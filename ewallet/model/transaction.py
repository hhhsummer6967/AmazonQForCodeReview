from datetime import datetime
from enum import Enum
import string

import re

class TransactionType(Enum):
  """
  Enumerates the type of a monetary transaction.
  """

  TOP_UP = 'TOP_UP'
  """When a user top ups their account."""
  TRANSFER = 'TRANSFER'
  """When a user transfers money to another user."""
  PAYMENT = 'PAYMENT'
  """When a user makes a payment using their wallet as payment method."""
  REFUND = 'REFUND'
  """When a user receives a refund from a payment."""
  WITHDRAWAL = 'WITHDRAWAL'
  """When a user withdraws their funds from their wallet."""

class TransactionStatus(Enum):
  """
  Enumerates the status of a monetary transaction.
  """

  PENDING = 'PENDING'
  """When a transaction is being processed."""
  COMPLETED = 'COMPLETED'
  """When a transaction is successfully completed."""
  FAILED = 'FAILED'
  """When a transaction fails."""
  CANCELLED = 'CANCELLED'
  """When a transaction is cancelled by the user or the system."""

class Transaction:
  """
  This class represents an electronic monetary transaction,
  created when someones makes or receives payment.
  """

  def __init__(self, wallet, amount: float, currency: str, type: TransactionType):
    """
    When a new Transaction is created, its `created_at` attribute
    is automatically set as the current timestamp.
    It's also initiated with the status `PENDING`.

    :param Wallet wallet: The wallet to which the transaction belongs.
    :param float amount: The monetary value of the transaction.
    :param str currency: The ISO-4217 currency code of the transaction.
    :param TransactionType type: The type of transaction.
    """
    self.id = None
    self.wallet = wallet
    self.amount = amount
    self.currency = currency
    self.type = type
    self.created_at = datetime.now()
    self.status = TransactionStatus.PENDING

  @property
  def formatted_amount(self) -> str:
    """
    Returns the formatted monetary value of the transaction
    with 2 decimal digits, including the currency code.

    :return: The formatted monetary value of the transaction.
    :rtype: str
    """
    return f'{self.amount:.2f} {self.currency}'

  def is_valid_currency_code(code):
    if type(code) != str:
      return False

    code = code.upper()

    if len(code) != 3:
      return False

    for char in code:
      if char not in string.ascii_uppercase:
        return False

    return True
