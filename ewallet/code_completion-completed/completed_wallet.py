from ewallet.model.transaction import Transaction, TransactionType
import csv

class Wallet:
  """
  This class represents an e-wallet.
  It holds a balance in different currencies.
  Users can perform operations on the wallet such as
  top up, withdrawal, transfers, and payments.
  Each wallet contains a list of transactions represented by the `Transaction` class.
  """
  def __init__(self, name: str):
    """
    Initiates a wallet with no balance and an empty list of transactions.
    """
    self.balance = {}
    self.transactions = []
    self.id = None
    self.name = name

  def get_balance(self, currency) -> float:
    """
    Returns the balance of the wallet in the specified currency.
    :param str currency: The ISO-4217 currency code.
    :return: The balance of the wallet in the specified currency.
    :rtype: float
    """
    return self.balance.get(currency, 0.0)

  def list_balance(self) -> list[str]:
    """
    Returns a list of the wallet's balance in different currencies.
    Each item in the list is a string composed by the currency code
    and the amount with two decimals.
    :return: A list of the wallet's balance in different currencies.
    :rtype: list[str]
    """
    return [f"{currency} {amount:.2f}" for currency, amount in self.balance.items()]

  def has_sufficient_balance(self, amount: float, currency: str) -> bool:
    """
    Verifies if the wallet has sufficient balance to perform the transaction.
    :param float amount: The amount of the transaction.
    :param str currency: The ISO-4217 currency code.
    :raise ValueError: If the currency doesn't follow the ISO-4217 standard.
    :return: True if the wallet has sufficient balance, False otherwise.
    :rtype: bool
    """
    if not Transaction.is_valid_currency_code(currency):
      raise ValueError("The currency must follow the ISO-4217 standard.")

    return self.get_balance(currency) >= amount

  def add_transaction(self, amount: float, currency: str, type: TransactionType) -> Transaction:
    """
    Adds a transaction to the wallet and update its balance.
    :param float amount: The amount of the transaction.
    :param str currency: The ISO-4217 currency code.
    :param TransactionType type: The type of transaction.
    :raise ValueError: If the currency doesn't follow the ISO-4217 standard.
    :return: The transaction object.
    :rtype: Transaction
    """
    if not Transaction.is_valid_currency_code(currency):
      raise ValueError("The currency must follow the ISO-4217 standard.")

    transaction = Transaction(self, amount, currency, type)
    self.transactions.append(transaction)
    self.balance[currency] = self.get_balance(currency) + amount
    return transaction

  def transfer(self, amount: float, currency: str, destination_wallet: 'Wallet') -> tuple[Transaction]:
    """
    Transfers the specified amount from the origin wallet
    to the destination wallet if the origin wallet has enough balance.
    A new transaction is created in the wallet with a negative amount.
    A new transaction is created in the destination wallet with a positive amount.
    :param float amount: The amount to transfer.
    :param str currency: The ISO-4217 currency code.
    :param Wallet destination_wallet: The destination wallet.
    :raise ValueError: If the currency doesn't follow the ISO-4217 standard.
    :raise ValueError: If the wallet doesn't have sufficient funds.
    :return: A tuple of the transaction objects.
    :rtype: tuple[Transaction]
    """
    if not self.has_sufficient_balance(amount, currency):
      raise ValueError("Insufficient funds.")

    transaction = self.add_transaction(-amount, currency, TransactionType.TRANSFER)
    destination_transaction = destination_wallet.add_transaction(amount, currency, TransactionType.TRANSFER)
    return transaction, destination_transaction

  def withdraw(self, amount: float, currency: str) -> Transaction:
    """
    Withdraws the specified amount from the wallet
    if the wallet has enough balance.
    A new transaction is created in the wallet with a negative amount.
    :param float amount: The amount to withdraw.
    :param str currency: The ISO-4217 currency code.
    :raise ValueError: If the currency doesn't follow the ISO-4217 standard.
    :raise ValueError: If the wallet doesn't have sufficient funds.
    :return: The transaction object.
    :rtype: Transaction
    """
    if not self.has_sufficient_balance(amount, currency):
      raise ValueError("Insufficient funds.")

    return self.add_transaction(-amount, currency, TransactionType.WITHDRAWAL)

  def top_up(self, amount: float, currency: str) -> Transaction:
    """
    Top up the wallet with the specified amount and currency.
    :param float amount: The amount to top up.
    :param str currency: The ISO-4217 currency code.
    :raise ValueError: If the currency doesn't follow the ISO-4217 standard.
    :return: The transaction object.
    :rtype: Transaction
    """
    return self.add_transaction(amount, currency, TransactionType.TOP_UP)

  # function to get total number of transactions of the wallet
  def get_total_transactions(self) -> int:
    """
    Returns the total number of transactions in the wallet.
    :return: The total number of transactions in the wallet.
    :rtype: int
    """
    return len(self.transactions)

  # function to filter out transaction list based on transaction type
  def filter_transactions(self, transaction_type: TransactionType) -> list[Transaction]:
    """
    Returns a list of transactions filtered by transaction type.
    :param TransactionType transaction_type: The transaction type to filter by.
    :return: A list of transactions filtered by transaction type.
    :rtype: list[Transaction]
    """
    return [transaction for transaction in self.transactions if transaction.type == transaction_type]
