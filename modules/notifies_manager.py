import json
import requests, os, dotenv

dotenv.load_dotenv()

class TeleNotify:
    def __init__(self, status: bool = True) -> None:
        self.status = status
        self.TOKEN = os.getenv('BOT_TOKEN')
        self.CHAT_ID = os.getenv('CHAT_ID')

    def send_message(self, title: str, message: str) -> int:
        if self.status:
            msg = f'*{title}*\n{message}'
            url = f"https://api.telegram.org/bot{self.TOKEN}/sendMessage"
            payload = {
                'chat_id': self.CHAT_ID,
                'text': msg,
                'parse_mode': 'Markdown'
            }
            
            resp = requests.post(url, json=payload)
            return resp.status_code
        else:
            pass
    
    def bot_status(self, message: str):
        status_code = self.send_message('🔔Bot status!', message)
        return status_code
    
    def bought(self, message: str):
        status_code = self.send_message('📉Buy!', message)
        return status_code

    def sold(self, message: str):
        status_code = self.send_message('📈Sell!', message)
        return status_code

    def error(self, message: str):
        status_code = self.send_message('❌Error!', message)
        return status_code

    def warning(self, message: str):
        status_code = self.send_message('⚠️Warning!', message)
        return status_code
    
class NotifyManager():
    def __init__(self):
        self.telenotify = TeleNotify(True)

    def _get_cant_buy_notify_status(self):
        with open('src/temp.json') as f:
            temp = json.load(f)
            return temp.get('cantBuyNotify')
        
    def update_cant_buy_notify_status(self, status: bool):
        with open('src/temp.json') as f:
                temp = json.load(f)
                temp['cantBuyNotify'] = status
                
        with open('src/temp.json', 'w') as f:
            json.dump(temp, f, indent=4)

    def invalid_balance(self):
        if self._get_cant_buy_notify_status():
            self.telenotify.warning('Not enough balance for averaging! Waiting for sell...')
            self.update_cant_buy_notify_status(False)

