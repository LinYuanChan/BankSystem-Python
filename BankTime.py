"""
Time Class
"""
import _datetime


class BankDate:
    year = 2000
    month = 1
    day = 1


    def __init__(self, date_in):
        try:
            args = date_in.split('/')
            # print(args)
            self.year = int(args[0])
            self.month = int(args[1])
            self.day = int(args[2])
            self.date = _datetime.date(self.year, self.month, self.day)
        except BaseException:
            raise

    def is_leap(self):
        # judge if a year is leap year
        if self.year % 100 == 0 & self.year % 400 == 0:
            # is divisible by 400
            return True
        if self.year % 100 & self.year % 4 == 0:
            # isn't divisible by 100 but 4
            return True
        return False

    def cal_delta_day(self, m_op_date):
        self_date = _datetime.date(self.year, self.month, self.day)
        op_date = _datetime.date(m_op_date.year, m_op_date.month, m_op_date.day)
        interval = self_date - op_date
        return interval.days


class BankDater:
    pass


if __name__ == '__main__':
    b = BankDate("2022/-9/p")
    c = BankDate("2022/12/4")
    print(c.cal_delta_day(b))
