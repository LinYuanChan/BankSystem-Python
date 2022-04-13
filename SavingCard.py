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
            self.last_date = create_date
        except BaseException:
            raise Exception("Invalid date format")

    def flash_sum(self, new_date):
        delta_day = new_date.cal_delta_day(self.create_date)
        self.daily_sum += delta_day * self.balance
        self.last_date = new_date

    def deposit(self, trade):
        """Deposit func"""
        if trade.amount < 0:
            raise Exception("Amount < 0")
        if not isinstance(trade.amount, int):
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
            if cur.date_.cal_delta_day(st_date) > 0:
                ret.append(cur.get_info())
        return ret

    def settle(self, st_date):
        self.flash_sum(st_date)
        if st_date.is_leap():
            interest = self.daily_sum / 366 * self.rate
        else:
            interest = self.daily_sum / 365 * self.rate
        settle_trade = Trade.Trade(st_date, interest, "Settle Interest")
        self.deposit(settle_trade)

        delta_year = st_date.year - self.last_date.year
        if delta_year:
            for i in range(delta_year):
                self.pay_annual_fee(BankTime.BankDate(str(i + 1) + "/1/1"))

    def pay_annual_fee(self, pay_date):
        self.flash_sum(pay_date)
        annual_fee_trade = Trade.Trade(pay_date, self.annual_fee, "pay annual fee")
        self.withdraw(annual_fee_trade)

    def monthly_income(self, query_date):
        ret = 0
        for trade in self.trades:
            if trade.date_.year == query_date.year and trade.date_.month == query_date.month:
                if trade.trade_type == "deposit":
                    ret += trade.amount
        return ret

    def monthly_expand(self, query_date):
        ret = 0
        for trade in self.trades:
            if trade.date_.year == query_date.year and trade.date_.month == query_date.month:
                if trade.trade_type == "withdraw":
                    ret += trade.amount
        return ret
