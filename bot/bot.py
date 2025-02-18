from client.bases import BotBase
from logging import getLogger
from logic.averating import Averating
from logic.first_buy import Buy
from logic.sell import Sell

from modules.stab_manager import TempBalanceManager, TempKlinesManager


logger = getLogger(__name__)


class Bot(BotBase):
    def __init__(self) -> None:
        super().__init__()
        self.temp_balance = TempBalanceManager()
        self.averating_script = Averating()
        self.buy_script = Buy()
        self.sell_script = Sell()
        self.temp_klines = TempKlinesManager()

    def activate(self):
        logger.info(f'Bot activated. Pair: {self.symbol}, balance: {self.temp_balance.get()["USDT"]}')
        self.notify.bot_status(f'Bot **activated**.\nPair: {self.symbol}\nBalance: {self.temp_balance.get()["USDT"]}')

        while True:

            self.temp_balance.update()
            self.temp_klines.update()
            self.buy_script.activate()
            self.averating_script.activate()
            self.sell_script.activate()
    # def start(self) -> None:
    #     while True:
    #             time.sleep(3)
    #             self.profit_edit.add_profit()
    #             balance = self.account.get_balance()

    #             #Первая покупка
    #             if self.orders.qty() == 0:
    #                 logger.debug('trying "first buy"')
    #                 if float(balance.get('USDT')) > self.amount_buy:
    #                     logger.debug('activating first buy script')
    #                     self.buy_script.activate()

    #             #Усреднение
    #             if self.orders.qty() != 0:
    #                 logger.debug('trying "averaging"')
    #                 if float(balance.get('USDT')) > self.amount_buy: 
    #                     logger.debug('activating averaging script')
    #                     self.averating_script.activate()

    #             if self.lines.sell_lines_qty() > 0:
    #                 logger.debug('sell lines qty > 0. Activating sell script')
    #                 if self.sell_script.activate():
    #                     self.sell_notify()

    #             if self.orders.qty() != 0:
    #                 if self.nem_notify_status == False:
    #                     if(float(balance.get('USDT')) < self.amount_buy):
    #                         self.notifies_edit.not_enough_money_notify()



bot = Bot()