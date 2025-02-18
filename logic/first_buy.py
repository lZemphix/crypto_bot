from modules.stab_manager import LinesManager, TempOrdersManager, TempBalanceManager
from client.bases import BotBase
from client.orders import Orders
from client.klines import Klines
from logging import getLogger
import ta.momentum
import ta

logger = getLogger(__name__)

class Buy(BotBase):
    
    def __init__(self):
        super().__init__()
        self.orders = Orders()
        self.lines = LinesManager()
        self.temp_orders = TempOrdersManager()
        self.temp_balance = TempBalanceManager()
        self.klines = Klines()

    def _get_rsi(self):   
        df = self.klines.get_klines_dataframe()
        rsi = ta.momentum.rsi(df.close).iloc[-1]
        return rsi
    
    def __notify(self):
        last_order = self.orders.get_order_history()[0].get('cumExecValue')
        balance = self.temp_balance.get_updated()
        min_sell_price = self.lines.get_sell_lines()[0]
        min_buy_price = self.lines.get_buy_lines()[0] 
        logger.info(f'First buy for ${last_order}. Balance: {balance["USDT"]}. Min price for sell: ${min_sell_price}. Min price for averate: ${min_buy_price}')
        self.notify.bought(f'First buy for ${last_order}\nBalance: {balance["USDT"]}\nMin price for sell: ${min_sell_price}\nMin price for averate: ${min_buy_price}')

    def activate(self) -> None:
        actual_rsi = self._get_rsi()
        orders_qty = self.temp_orders.get_qty()
        if actual_rsi < self.RSI and orders_qty == 0:
            if self.orders.place_buy_order() == True:
                self.temp_orders.update_orders()
                self.__notify()                
            