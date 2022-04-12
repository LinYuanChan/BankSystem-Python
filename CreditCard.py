"""
Credit Card Class
"""
import BankTime
import Trade


class CreditCard:
    account_name = ""
    balance = 0.0
    credit = 0.0
    annual_fee = 0
    rate = 0.0
    daily_sum = 0
    trades = []

    def __init__(self, account_name, balance, credit, annual_fee, rate, create_date):
        """Init account name"""
        # check valid
        if annual_fee < 0:
            raise Exception("Invalid annual fee!", annual_fee)
        if rate < 0 or rate > 1:
            raise Exception("Invalid rate!", rate)
        if balance < 0:
            raise Exception("Invalid balance!", balance)
        if credit < 0:
            raise Exception("Invalid credit!", credit)

        # init members
        self.annual_fee = annual_fee
        self.balance = balance
        self.account_name = account_name
        self.rate = rate
        self.credit = credit

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
        if not isinstance(trade.amount, int):
            raise Exception("Amount Type Error!")
        self.flash_sum(trade.date_)
        self.balance -= trade.amount
        self.trades.append(trade)

    def query(self, st_date):
        ret = []
        for cur in self.trades:
            if(cur.date_.cal_delta_day(st_date) > 0):
                ret.append(cur.get_info())
        return ret

    def settle(self, st_date):
        self.flash_sum(st_date)
        # todo: leap year
        interest = self.daily_sum / 365 * self.rate
        settle_trade = Trade.Trade(st_date, interest, "Settle Interest")
        self.withdraw(settle_trade)

    def pay_annual_fee(self, pay_date):
        self.flash_sum(pay_date)
        annual_fee_trade = Trade.Trade(pay_date, self.annual_fee, "pay annual fee")
        self.withdraw(annual_fee_trade)

