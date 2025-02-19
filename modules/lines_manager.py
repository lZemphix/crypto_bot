from modules.stab_manager import (LinesManager, 
                                  TempKlinesManager)


class CrossLines:

    def __init__(self):
        self.klines = TempKlinesManager()
        self.lines = LinesManager()
        pass

    def __get_data(self):
        klines = self.klines.get_updated()
        buy_lines = self.lines.get_buy_lines()
        sell_lines = self.lines.get_sell_lines()
        pre_pre_last_kline = float(klines[2][4])
        pre_last_kline = float(klines[1][4])

        return buy_lines, sell_lines, pre_last_kline, pre_pre_last_kline
    
    def cross_down_to_up(self): # Покупка
        buy_lines, _, pre_last_kline, pre_pre_last_kline = self.__get_data()
        
        for buy_line in buy_lines[::-1]:
            if pre_last_kline > buy_line: # Цена последней свечи выше линии
                if pre_pre_last_kline < buy_line: # Цена предпоследней свечи ниже чем линия продажи
                    if pre_last_kline > pre_pre_last_kline: # Цена последней свечи выше чем свечи до нее
                        print(buy_line)
                        return True
        return False
    
    def cross_up_to_down(self): # Продажа
        _, sell_lines, pre_last_kline, pre_pre_last_kline = self.__get_data()
        # print('asdsad')
        for sell_line in sell_lines:
            # print(buy_line)
            if pre_last_kline < sell_line: # Цена последней свечи ниже линии
                # print('p')
                if pre_pre_last_kline > sell_line: # Цена предпоследней свечи выше чем линия продажи
                    # print('m')
                    if pre_last_kline < pre_pre_last_kline: # свеча красная
                        print(sell_line)
                        return True
        return False

