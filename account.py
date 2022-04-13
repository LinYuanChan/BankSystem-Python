"""
Account Class
"""
import base64
import re
import SavingCard
import CreditCard


def password_checker(usr_password):
    HAS_AT_LEAST_THREE_KINDS_CHARS = re.compile("(?![a-z0-9]+$)")

    if len(usr_password) > 40:
        raise Exception("Invalid password(length)!", usr_password, len(usr_password))
    if usr_password.isspace():
        raise Exception("Invalid password(is space)!")
    if not HAS_AT_LEAST_THREE_KINDS_CHARS.search(usr_password):
        raise Exception("Invalid password(too simple)!")


def usr_name_checker(usr_name):
    ONLY_NUM_AND_LETTER = re.compile("^(?!\d+$)[\da-zA-Z_]+$")
    FIRST_CHAR_IS_LETTER = re.compile("^[a-zA-Z]")
    if len(usr_name) > 20:
        raise Exception("Invalid username(length)!", usr_name, len(usr_name))
    if usr_name.isspace():
        raise Exception("Invalid username(is space)!")
    if not ONLY_NUM_AND_LETTER.search(usr_name):
        raise Exception("Invalid username(special char)!", usr_name)
    if not FIRST_CHAR_IS_LETTER.search(usr_name):
        raise Exception("Invalid username(invalid first char)!", usr_name[0])


class Account:
    usr_name = ""
    usr_password_base64 = ""
    credit_card = None
    saving_card = None

    def __init__(self, usr_name, usr_password):
        try:
            usr_name_checker(usr_name)
            password_checker(usr_password)
        except Exception:
            raise Exception("Create Failed")
        else:
            self.usr_name = usr_name
            password_utf8 = usr_password.encode('utf-8')
            self.usr_password_base64 = base64.b64encode(password_utf8)

    def create_sav_card(self, account_name, balance, annual_fee, rate, create_date):
        try:
            self.saving_card = SavingCard.SavingCard(account_name, balance, annual_fee, rate, create_date)
        except Exception:
            raise Exception("Create Failed")

    def create_cre_card(self, account_name, balance, credit, annual_fee, rate, create_date):
        try:
            self.credit_card = CreditCard.CreditCard(account_name, balance, credit, annual_fee, rate, create_date)
        except Exception:
            raise Exception("Create Failed")

    def query_trades(self, st_date, mode):
        """
        modes:
            0: All Available Accounts
            1: Saving Account
            2: Credit Account
        """
        if mode == 0:
            ret_sav = self.saving_card.query(st_date)
            ret_cre = self.credit_card.query(st_date)
            ret = ret_cre + ret_sav
        elif mode == 1:
            ret = self.saving_card.query(st_date)
        elif mode == 2:
            ret = self.credit_card.query(st_date)
        else:
            raise Exception("Invalid Query Mode", mode)
        return ret

    def gen_monthly_report(self, query_date):
        if self.saving_card is not None:
            self.saving_card.monthly_expand(query_date)
            self.saving_card.monthly_income(query_date)
        if self.credit_card is not None:
            self.credit_card.monthly_expand(query_date)
            self.credit_card.monthly_income(query_date)

if __name__ == "__main__":
    acc = Account("sds", "Sad123")
    print(acc.usr_password_base64)
