from logging import getLogger
import time
from client.bases import BotBase
from client.klines import Klines
from client.orders import Orders
from modules.lines_manager import CrossLines
from modules.notifies_manager import NotifyManager, TeleNotify
from modules.stab_manager import LinesManager, TempBalanceManager, TempKlinesManager, TempOrdersManager, LapsManager

logger = getLogger(__name__)

class Sell(BotBase):
     
    def __init__(self) -> None:
        super().__init__()
        self.klines = Klines()
        self.temp_orders = TempOrdersManager()
        self.orders = Orders()
        self.cross = CrossLines()
        self.notifies_manager = NotifyManager()
        self.laps = LapsManager()
        self.telenotify = TeleNotify()
        self.lines = LinesManager()
        self.temp_klines = TempKlinesManager()

        
    def get_rsi(self) -> None:
        import ta
        df = self.klines.get_klines_dataframe()
        actual_rsi = ta.momentum.rsi(df.close).iloc[-1]
        return actual_rsi  
      
    def price_valid(self):
        actual_price = float(self.temp_klines.get_updated()[0][4])
        sell_price = self.temp_orders.get_avg_order() + self.stepSell
        actual_price_higher = sell_price <= actual_price        
        return actual_price_higher

    def rsi_valid(self):
        rsi = self.get_rsi()
        return rsi > self.RSI + 1
    
    def __notify(self):
        last_order = self.orders.get_order_history()[0]
        last_order_price = float(last_order['cumExecValue'])
        coin_qty = float(last_order['cumAExecQty'])
        coin_name = self.symbol.replace('USDT')
        self.telenotify.sold(f'Bot was sold {coin_qty} {coin_name} for {last_order_price}.\nTotal: price: {coin_qty*last_order_price}')

    def activate(self) -> bool:
        if self.temp_orders.get_qty() > 1:
            if self.rsi_valid():
                if self.price_valid():
                    if self.cross.cross_up_to_down():
                        if self.orders.place_sell_order():
                            self.notifies_manager.update_cant_buy_notify_status(True)
                            self.temp_orders.clear()
                            self.lines.clear()
                            self.laps.add_one()
                            self.__notify()
                            time.sleep(2)

