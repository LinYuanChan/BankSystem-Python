class Trade:
    def __init__(self, date_, amount, desc):
        self.date_ = date_
        self.amount = amount
        self.desc = desc

    def get_info(self):
        ret = self.date_ + "\t" + str(self.amount) + "\t" + self.desc
        return ret
