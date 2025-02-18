from logging import getLogger
from client.bases import Client
from client.account import Account

logger = getLogger(__name__)

class Orders(Client):
    def __init__(self):
        super().__init__()
        self.account = Account()

    def get_order_history(self) -> dict | int:
        """cancelType: [CancelByUser | UNKNOWN]
        cumExecValue: [float] - in usdt
        cumExecQty [float] - in second coin"""
        try:
            history = self.client.get_order_history(category='spot')['result']['list']
            return history
        except:
            return 1
        
    def get_open_orders(self):
        try:
            open_orders = self.client.get_open_orders(category='spot')['result']['list']
            return open_orders
        except: 
            return 1
    
    def place_buy_order(self) -> bool:
        try:
            self.client.place_order(
                category='spot',
                symbol=self.symbol,
                side='Buy',
                orderType='Market',
                qty=self.amount_buy,
            )
            return True
        except Exception as e:
            logger.error(e)
            return False

    def place_sell_order(self) -> bool:
        try:
            coin_name = self.symbol.replace('USDT', '')
            amount = float(self.account.get_balance().get(coin_name)[:4])
            self.client.place_order(
                category='spot',
                symbol=self.symbol,
                side='Sell',
                orderType='Market',
                qty=amount
            )
            return True
        except Exception as e:
            logger.error(e)

        
    