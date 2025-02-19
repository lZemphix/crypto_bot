from logging import getLogger
import time
from client.orders import Orders    
from modules.lines_manager import CrossLines
from modules.notifies_manager import NotifyManager
from modules.stab_manager import LinesManager, TempBalanceManager, TempKlinesManager, TempOrdersManager
from client.bases import BotBase, get_bot_config
from client.klines import Klines

logger = getLogger(__name__)

class Averating(BotBase):

    def __init__(self) -> None:
        super().__init__()
        self.klines = Klines()
        self.temp_balance = TempBalanceManager()
        self.temp_orders = TempOrdersManager()
        self.temp_klines = TempKlinesManager()
        self.orders = Orders()
        self.cross = CrossLines()
        self.lines = LinesManager()
        self.notifies_manager = NotifyManager()

    def get_rsi(self):
        import ta
        df = self.klines.get_klines_dataframe()
        rsi = ta.momentum.rsi(df.close).iloc[-1]
        return rsi
    
    def valid_balance(self):
        usdt_balance = self.temp_balance.get_updated()['USDT']
        amount_buy_price = get_bot_config('amountBuy')
        
        return True if usdt_balance > amount_buy_price else False
    
    def valid_price(self):
        avg_order = self.temp_orders.get_avg_order()
        actual_price = float(self.temp_klines.get_updated()[0][4])
        step_buy = get_bot_config('stepBuy')
        step_higher = step_buy > (actual_price - avg_order)
        print(f"{step_buy=}", f"{actual_price=}", f"{avg_order=}")
        return True if (actual_price < avg_order and step_higher) else False

    def __notify(self):
        last_order = self.orders.get_order_history()[0].get('cumExecValue')
        balance = self.temp_balance.get_updated()
        min_sell_price = self.lines.get_sell_lines()[0]
        min_buy_price = self.lines.get_buy_lines()[0] 
        logger.info(f'Averating for ${last_order}. Balance: {balance["USDT"]}. Min price for sell: ${min_sell_price}. Min price for next averating: ${min_buy_price}')
        self.notify.bought(f'Averating for ${last_order}\nBalance: {balance["USDT"]}\nMin price for sell: ${min_sell_price}\nMin price for next averating: ${min_buy_price}')


    def activate(self) -> None:
        if self.get_rsi() < self.RSI:
            if self.valid_balance():
                if self.cross.cross_down_to_up():                        
                    if self.valid_price():
                        if self.orders.place_buy_order():
                            if self.temp_orders.update_orders():
                                self.__notify()
                                time.sleep(2)
            else:
                self.notifies_manager.invalid_balance() 

                