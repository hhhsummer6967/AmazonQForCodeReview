import unittest
import sys
sys.path.append('.')

import boto3
from ewallet.model.wallet import Wallet
from ewallet.model.transaction import TransactionType, TransactionStatus

class WalletTest(unittest.TestCase):

  def test_wallet_creation(self):
    wallet = Wallet('test_wallet')
    self.assertDictEqual(wallet.balance, {})
    self.assertCountEqual(wallet.transactions, [])
    self.assertEqual(wallet.id, None)
    self.assertEqual(wallet.name, 'test_wallet')

  def test_list_balance(self):
    wallet = Wallet('test_wallet')
    wallet.add_transaction(100, 'USD', TransactionType.TOP_UP)
    wallet.add_transaction(300, 'EUR', TransactionType.TOP_UP)
    wallet.add_transaction(50, 'GBP', TransactionType.TOP_UP)
    wallet.withdraw(50, 'GBP')

    balance = wallet.list_balance()

    self.assertListEqual(balance, ['USD 100.00', 'EUR 300.00', 'GBP 0.00'])

  # create a function that tests top_up
  def test_top_up(self):
    wallet = Wallet('test_wallet')
    wallet.top_up(100, 'USD')
    self.assertEqual(wallet.balance['USD'], 100)
    self.assertEqual(len(wallet.transactions), 1)
    self.assertEqual(wallet.transactions[0].amount, 100)
    self.assertEqual(wallet.transactions[0].currency, 'USD')
    self.assertEqual(wallet.transactions[0].type, TransactionType.TOP_UP)

  def test_transfer_balances(self):
    # arrange
    wallet1 = Wallet('wallet1')
    wallet2 = Wallet('wallet2')

    wallet1.top_up(100, 'USD')

    # act
    wallet1.transfer(50, 'USD', wallet2)

    # assert balances
    self.assertEqual(wallet1.balance['USD'], 50)
    self.assertEqual(wallet2.balance['USD'], 50)
