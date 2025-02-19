from cfg.config import get_bot_config
from client.account import Account
from client.bases import StabBase
from client.klines import Klines
from client.orders import Orders
from logging import getLogger
import json

logger = getLogger(__name__)

class TempManager(StabBase):
    def __init__(self):
        super().__init__()

    def read(self) -> dict | int:
        try:
            with open(self.path) as f:
                file = json.load(f)
                return file
        except Exception as e:
            logger.error(e)
            return 1

    def update(self, **kwargs) -> int:
        try:
            with open(self.path) as f:
                temp = json.load(f)
                for key, value in kwargs.items():
                    temp[key] = value

            with open(self.path, 'w') as f:
                json.dump(temp, f, indent=4)
                return 0  
            
        except Exception as e:
            logger.error(e)
            return 1

class TempBalanceManager(StabBase):
    def __init__(self):
        super().__init__()
        self.account = Account()
        self.temp_manager = TempManager()

    def _get_valid_balance(self) -> bool:
        try:
            balance = self.account.get_balance()
            return balance if balance != {} else False
        except:
            return False

    def update(self) -> None:
        balance = self._get_valid_balance()
        if balance != False:
            self.temp_manager.update(balance=balance)

    def get(self):
        with open(self.path) as f:
            temp = json.load(f)
            return temp.get('balance')
        
    def get_updated(self):
        self.update()
        return self.get()

class TempKlinesManager(StabBase):
    def __init__(self):
        super().__init__()
        self.temp_manager = TempManager()
        self.klines = Klines()

    def _get_valid_klines(self):
        try:
            klines = self.klines.get_klines()
            return klines if type(klines) == list else False
        except:
            pass
    
    def update(self):
        klines = self._get_valid_klines()
        if klines != False:
            self.temp_manager.update(klines=klines)

    def get(self):
        with open(self.path) as f:
            temp = json.load(f)
            return temp.get('klines')
        
    def get_updated(self):
        self.update()
        return self.get()

class TempOrdersManager(StabBase):
    def __init__(self):
        super().__init__()
        self.temp_manager = TempManager()
        self.orders = Orders()

    def clear(self):
        self.temp_manager.update(orders=[])
        
    def _read_last_order_id(self):
        with open(self.path) as f:
            temp = json.load(f)
            return temp.get('lastOrderId')
        
    def _get_orders(self):
        orders = self.read_orders() # получение списка ордеров из темпа
        last_order_id = self._read_last_order_id() # получения айди последнего ордера из темпа
        actual_exec_order = self.orders.get_order_history()[0] # Получение актуального ордера
        actual_order_id = actual_exec_order.get('orderId') # Получение актуального айди ордера
        if actual_exec_order.get('side') == 'Buy' and actual_order_id != last_order_id: # покупка и айди актуального не совпадает с айди из темпа
            last_exec_order_value = float(actual_exec_order.get('avgPrice')) # Перевод исполненной цены в юсдт из актуального ордера во флоат
            orders.append(last_exec_order_value) # Добавление нового ордера в список ордеров, полученного из темпа
            self.temp_manager.update(lastOrderId=actual_order_id) # Запись айди последнего ордера
            return orders
        else:
            return False
        
    def read_orders(self) -> list:
        temp = self.get_temp()
        return temp.get('orders')
        
    def update_orders(self):
        orders = self._get_orders()
        if orders != False:
            self.temp_manager.update(orders=orders)
            return True

    def get_qty(self):
        orders = self.read_orders()
        return len(orders)

    def get_avg_order(self) -> float:
        orders = self.read_orders()
        avg_orders = sum(orders) / self.get_qty() if self.get_qty() != 0 else 1
        return round(avg_orders , 3)

class LapsManager(StabBase):
    def __init__(self):
        super().__init__()
        self.temp_manager = TempManager()
    
    def get(self):
        temp = self.get_temp()
        return temp.get('laps')

    def clear(self):
        self.temp_manager.update(laps=0)
        return True
    
    def add_one(self):
        laps = self.get()
        self.temp_manager.update(laps=laps+1)
        return True


class LinesManager(StabBase):
    def __init__(self):
        super().__init__()

    def __read_lines(self, line_type: str):
        with open(f'src/{line_type}_lines') as f:
            lines = f.readlines()
            lines = self.__formating(lines)
            return lines
        
    def __formating(self, data: list[str]) -> list[float]:
        return [round(float(float_el),3) for float_el in [el.replace('\n', '') for el in data]]
        
    def __create_lines(self, order_price: float):
        """sell buy"""
        sell_lines, buy_lines = [], []
        step_buy =  get_bot_config('stepBuy')
        step_sell = get_bot_config('stepSell')
        for i in range(50):
            sell_lines.append(round(order_price+step_sell*(i+1), 3))
            buy_lines.append(round(order_price-step_buy*(i+1),3))
        return sell_lines, buy_lines
    
    def get_sell_lines(self):
        return self.__read_lines('sell')

    def get_buy_lines(self):
        return self.__read_lines('buy')
    
    def write_lines(self, order_price: float):
        sell_lines, buy_lines = self.__create_lines(order_price)
        with open('src/buy_lines', 'w') as buy:
                with open('src/sell_lines', 'w') as sell:
                    for sells, buys in zip(sell_lines, buy_lines):
                        buy.write(f'{buys}\n')
                        sell.write(f'{sells}\n')

    def clear(self):
        with open('src/buy_lines', 'w') as f:
            f.write()
        with open('src/sell_lines', 'w') as f:
            f.write()
        return True


