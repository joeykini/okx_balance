import os
import time
import requests
from dotenv import load_dotenv
from pyokx import OKXClient, Account

# 加载 .env 文件中的环境变量
load_dotenv()

# 创建 OKXClient 实例
client = OKXClient(
    key=os.getenv('OKX_API_KEY'),
    secret=os.getenv('OKX_SECRET_KEY'),
    passphrase=os.getenv('OKX_PASSPHRASE')
)

# Telegram Bot 配置
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# 函数：获取账户余额信息
def get_account_balance():
    try:
        account = Account(client)
        balance = account.get_balance().response.json()
        return balance
    except Exception as e:
        print("Error getting account balance:", e)
        return None

# 函数：发送 Telegram 通知
def send_telegram_notification(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        params = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return True
        else:
            print("Failed to send Telegram notification:", response.text)
            return False
    except Exception as e:
        print("Error sending Telegram notification:", e)
        return False

# 主循环：每5分钟查询一次账户余额，并发送 Telegram 通知
while True:
    account_balance = get_account_balance()
    if account_balance:
        # 打印账户余额信息
        print("Retrieved account balance:", account_balance)

        # 处理账户余额数据
        balances = account_balance.get('data', [])
        if balances:
            balance_message = "Account Balance:\n"
            for balance in balances:
                currency_details = balance.get('details', [])
                for detail in currency_details:
                    currency = detail.get('ccy', '')
                    amount = detail.get('availEq', '0')
                    balance_message += f"{currency}: {amount}\n"

            # 添加账户总余额的美元等值金额
            total_eq = balance.get('totalEq', 0)
            balance_message += f"\n账户余额 = {total_eq} USDT"

            # 发送 Telegram 通知
            if not send_telegram_notification(balance_message):
                print("Failed to send Telegram notification.")
        else:
            print("No balance data found.")

    # 等待5分钟
    time.sleep(300)