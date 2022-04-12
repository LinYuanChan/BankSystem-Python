"""
Saving Card Class
"""
import BankTime
import Trade


class SavingCard:
    account_name = ""
    balance = 0.0
    annual_fee = 0
    rate = 0.0
    daily_sum = 0
    trades = []

    def __init__(self, account_name, balance, annual_fee, rate, create_date):
        """Init account name"""
        # check valid
        if annual_fee < 0:
            raise Exception("Invalid annual fee!", annual_fee)
        if rate < 0 or rate > 1:
            raise Exception("Invalid rate!", rate)
        if balance < 0:
            raise Exception("Invalid balance!", balance)

        # init members
        self.annual_fee = annual_fee
        self.balance = balance
        self.account_name = account_name
        self.rate = rate

        try:
            self.create_date = BankTime.BankDate(create_date)
        except BaseException:
            raise Exception("Invalid date format")
        self.last_date = create_date

    def flash_sum(self, new_date):
        delta_day = new_date.cal_delta_day(self.create_date)
        self.daily_sum += delta_day * self.balance
        self.last_date = new_date

    def deposit(self, trade):
        """Deposit func"""
        if trade.amount < 0:
            raise Exception("Amount < 0")
        if isinstance(trade.amount, int) != True:
            raise Exception("Amount Type Error!")
        self.flash_sum(trade.date_)
        self.balance += trade.amount
        self.trades.append(trade)

    def withdraw(self, trade):
        """Withdraw func"""
        if trade.amount < 0:
            raise Exception("Amount < 0")
        if isinstance(trade.amount, int) != True:
            raise Exception("Amount Type Error!")
        self.flash_sum(trade.date_)
        self.balance -= trade.amount
        self.trades.append(trade)

