# ------------------- 你只需要改这里 -------------------
# 1. 换成你想监控的商品网址
URL = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html" 

# 2. 换成你的心理价位
TARGET_PRICE = 40.0
# ----------------------------------------------------

import requests, os
from bs4 import BeautifulSoup

def run_checker():
    BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

    try:
        page = requests.get(URL, headers={"User-Agent":"Mozilla/5.0"})
        soup = BeautifulSoup(page.content, "html.parser")
        
        # 你可能需要根据不同网站修改下面这行
        price_text = soup.find(class_="price_color").get_text()
        
        current_price = float(''.join(c for c in price_text if c.isdigit() or c == '.'))
        print(f"当前价格: {current_price}")
        
        if current_price < TARGET_PRICE:
            message = f"降价啦! 现在只要 {current_price} 元! 快去看看: {URL}"
            requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}")
            print("通知已发送!")

    except Exception as e:
        print(f"出错了: {e}")

if __name__ == "__main__":
    run_checker()