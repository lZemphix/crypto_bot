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
    
