import urllib.request as r
import json
import ctypes
import winsound
import threading
import os

symbolsBitmarket = ["BTC","BCC","LTC"]
symbols = ["BTC","BCC","BTG","LTC","ETH","DASH","GAME","LSK"]
p = 2

#bitbay.info i bitmarket.pl
def pobierz_ceny(url) :
    jsonurl = r.urlopen(url)

    data = jsonurl.read()
    output = json.loads(str(data,"UTF8"))

    ask = output['asks'][0]
    bid = output['bids'][0]

    return (ask,bid)

def pobierz_dane(url):
    req = r.Request(url, headers={'User-Agent': "Magic Browser"})
    jsonurl = r.urlopen(req)

    data = jsonurl.read()
    output = json.loads(str(data, "UTF8"))

    return output

def check_for_inefficiency():
    os.system('cls')

    #tylko dla pycharm
    print('\n' * 80)

    url_worldcoinindex = "https://www.worldcoinindex.com/apiservice/json?key=t7zj0MNVRpLUkNcvqW50IRcyTjcRZ0"
    data = pobierz_dane(url_worldcoinindex)
    markets = data['Markets']

    url_fixer = "https://api.fixer.io/latest?base=USD"
    curr_data = pobierz_dane(url_fixer)
    usd_to_pln = curr_data["rates"]["PLN"]


    for s in symbols:

        symbol = s
        global_symbol = ""

        #poprawka BCC na BCH dla worldcoin
        if s == "BCC":
            global_symbol = "BCH"
        else:
            global_symbol = s

        global_m = next(m for m in markets if m["Label"] == global_symbol + "/BTC")
        global_price_usd = global_m["Price_usd"]
        global_price_pln = global_price_usd * usd_to_pln

        url_bitbay = "https://bitbay.net/API/Public/"+symbol+"PLN/orderbook.json"
        ceny_bitbay = pobierz_ceny(url_bitbay)
        ask_bitbay = ceny_bitbay[0][0]
        bid_bitbay = ceny_bitbay[1][0]
        diff_bitbay = round((global_price_pln - ask_bitbay)*100/ask_bitbay,2)
        spread_bitbay=round((ask_bitbay - bid_bitbay)*100/bid_bitbay,2)

        if False: # s in symbolsBitmarket:
            url_bitmarket = "https://www.bitmarket.pl/json/"+symbol+"PLN/orderbook.json"
            ceny_bitmarket = pobierz_ceny(url_bitmarket)
            ask_bitmarket = ceny_bitmarket[0][0]
            bid_bitmarket = ceny_bitmarket[1][0]
            diff_bitmarket =  round((global_price_pln - ask_bitmarket) * 100 / ask_bitmarket,2)
            spread_bitmarket = round((ask_bitmarket - bid_bitmarket) * 100 / bid_bitbay, 2)

            print("Bitmarket " + s + ": " + str(ask_bitmarket) + " / " + str(bid_bitmarket) + " spread%: " + str(spread_bitmarket)
                  + " global: " +  str(global_price_pln) + " R: " + str(diff_bitmarket) + "%")

        print("Bitbay " + s + ": " + str(ask_bitbay) + " / " + str(bid_bitbay) + " spread%: " + str(spread_bitbay)
              + " global: " +  str(global_price_pln) + " R: " + str(diff_bitbay) + "%")

        if diff_bitbay>p:
            duration = 1000  # millisecond
            freq = 440  # Hz
            winsound.Beep(freq, duration)
            ctypes.windll.user32.MessageBoxW(0, str(diff_bitbay), "Okazja " + s, 1)

        #r = round((bid_bitbay-ask_bitmarket)*100.0/ask_bitmarket,2)
        #msg = "cena bitbay: " + str(bid_bitbay) + " cena bitmarket: " + str(ask_bitmarket) + " różnica: " + str(r) + "%"

        #if r>p:
        #   duration = 1000  # millisecond
        #   freq = 440  # Hz
        #   winsound.Beep(freq, duration)
        #  ctypes.windll.user32.MessageBoxW(0,msg , "Okazja "+symbol, 1)

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

set_interval(check_for_inefficiency,10)
check_for_inefficiency()

