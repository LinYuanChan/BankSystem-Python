class Trade:
    def __init__(self, date_, amount, trade_type, desc):
        self.date_ = date_
        self.trade_type = trade_type
        self.amount = amount
        self.desc = desc

    def get_info(self):
        ret = self.date_ + "\t" + str(self.amount) + "\t" + self.desc
        return ret
