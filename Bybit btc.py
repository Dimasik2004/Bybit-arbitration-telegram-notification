from time import sleep
from pybit import spot
import telebot
from telebot import types
bot = telebot.TeleBot(token='5522804791:AAGody6ry_cWIx0uc9p9wHVnIs0j7XkwbqY')
session = spot.HTTP(endpoint="https://api.bybit.com")

while(True):
    try:
        maxcoff = 0
        maxcoffcoinusdt = ""
        maxcoffcoinbtc = ""
        symbolBybit = session.latest_information_for_symbol()['result']
        bitcoin = ""
        for coins in symbolBybit:
            if "BTCUSDT" in coins['symbol']:
                bitcoin = coins['lastPrice']
        bitcoin = float(bitcoin)
        for coin in symbolBybit:
            if "BTC" in coin['symbol']:
                coinbtc = coin['symbol']
                coinbtc = coinbtc.replace("BTC", "")
                if "USDT" not in coinbtc:
                    for coinusdt in symbolBybit:
                        if "USDT" in coinusdt['symbol']:
                            if coinbtc in coinusdt['symbol']:
                                if(coinbtc == coinusdt['symbol'].replace("USDT", "")):
                                    try:
                                        coff1 = 1 / \
                                            float(coinusdt['lastPrice'])
                                        coff2 = coff1/float(coin['lastPrice'])
                                        coff3 = coff2*bitcoin
                                        if(coff3 > 20):
                                            coff2 = coff1 * \
                                                float(coin['lastPrice'])
                                            coff3 = coff2*bitcoin
                                            procent = (coff3-1)*100
                                        if(procent > maxcoff):
                                            maxcoff = procent
                                            maxcoffcoinusdt = coinusdt['symbol']
                                            maxcoffcoinbtc = coin['symbol']
                                    except:
                                        pass
                                    print(
                                        f"{coin['symbol']} {coin['lastPrice']}   {coinusdt['lastPrice']} {coinusdt['symbol']}    coff: {round(procent,2)}%\n")
        print(
            f"https://www.bybit.com/ru-RU/trade/spot/{maxcoffcoinusdt.replace('USDT','/USDT')}")
        print(
            f"https://www.bybit.com/ru-RU/trade/spot/{maxcoffcoinbtc.replace('BTC','/BTC')}")
        print(maxcoff)
        if(maxcoff > 0.8):
            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton(
                f'{maxcoffcoinusdt}', url=f"https://www.bybit.com/ru-RU/trade/spot/{maxcoffcoinusdt.replace('USDT','/USDT')}")
            btn2 = types.InlineKeyboardButton(
                f'{maxcoffcoinbtc}', url=f"https://www.bybit.com/ru-RU/trade/spot/{maxcoffcoinbtc.replace('BTC','/BTC')}")
            btn3 = types.InlineKeyboardButton(
                f'BTCUSDT', url=f"https://www.bybit.com/ru-RU/trade/spot/BTC/USDT")

            markup.add(btn1, btn2, btn3)
            bot.send_message(
                -1001558563045, f"USDT>{maxcoffcoinusdt.replace('USDT','')}>BTC>USDT\nPercent:{round(maxcoff,3)}%", reply_markup=markup)
        sleep(10)
    except:
        sleep(300)
