import json
import pandas as pd
from client.bases import Client

class Klines(Client):

    def __init__(self) -> None:
            super().__init__()

    def get_klines(self, limit: int = 200) -> dict:
        try:
            kline = self.client.get_kline(symbol=self.symbol, interval=self.interval, limit=limit, category='spot')
            return kline['result']['list']
        except:
            return 1

    def get_klines_dataframe(self) -> pd.DataFrame:
        try:
            with open('src/temp.json') as f:
                data = json.load(f)
                klines = data.get('klines')
            dataframe = pd.DataFrame(klines)
            dataframe.columns = ['time', 'open', 'high', 'low', 'close', 'volume', 'turnover']
            dataframe.set_index('time', inplace=True)
            dataframe.index = pd.to_numeric(dataframe.index, downcast='integer').astype('datetime64[ms]')    
            dataframe = dataframe[::-1]
            dataframe['close'] = pd.to_numeric(dataframe['close'])
            return dataframe
        except:
            return 1
