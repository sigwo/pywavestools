import requests
MAX_LINES = 30    # 0 for all
orders = requests.get("https://bittrex.com/api/v1.1/public/getorderbook?market=BTC-WAVES&type=both").json()['result']
grandtotal_bids_btc=0
grandtotal_bids_waves=0
grandtotal_asks_btc=0
grandtotal_asks_waves=0
buys = orders['buy']
sells = orders['sell']
for buy in buys:
	grandtotal_bids_btc+=buy['Quantity'] * buy['Rate']
	grandtotal_bids_waves+=buy['Quantity']
for sell in sells:
	grandtotal_asks_btc+=sell['Quantity'] * sell['Rate']
	grandtotal_asks_waves+=sell['Quantity']
buy_sum_waves = 0
buy_sum_btc = 0
sell_sum_waves = 0
sell_sum_btc = 0
print("-" * 200)
print("                                                      B I D                                           ||                                                  A S K")
print("                                                                                                      ||")
print("    #         Sum(BTC)         Sum(Waves)             Total         Size(Waves)           Bid(BTC)    ||          Ask(BTC)        Size(Waves)             Total          Sum(Waves)           Sum(BTC) ")
print("-" * 200)
for n in range(max(len(buys), len(sells))):
    if n>=MAX_LINES and MAX_LINES!=0:
        break
    line = "%5d " % (n + 1)
    if n < len(buys):
        buy_waves = buys[n]['Quantity']
        buy_rate = buys[n]['Rate']
        buy_total = buy_rate * buy_waves
        buy_sum_waves += buy_waves
        buy_sum_btc += buy_total
        line += "%18.8f %18.8f %18.8f %18.8f %18.8f  ||" % (buy_sum_btc, buy_sum_waves, buy_total, buy_waves, buy_rate)
    else:
        line += "                                                                                                ||"
    if n < len(sells):
        sell_waves = sells[n]['Quantity']
        sell_rate = sells[n]['Rate']
        sell_total = sell_rate * sell_waves
        sell_sum_waves += sell_waves
        sell_sum_btc += sell_total      
        line += "  %18.8f %18.8f %18.8f %18.8f %18.8f" % (sell_rate, sell_waves, sell_total, sell_sum_waves, sell_sum_btc)
    print(line)
   
print("-" * 200)
print
print("              %5d Buy orders" % len(buys))
print("              %5d Sell orders" % len(sells))
print
print(" %18.8f Total Bids (BTC)" % grandtotal_bids_btc)
print(" %18.8f Total Bids (Waves)" % grandtotal_bids_waves)
print(" %18.8f Average Bid (Waves)" % (grandtotal_bids_btc / grandtotal_bids_waves))
print
print(" %18.8f Total Asks (BTC)" % grandtotal_asks_btc)
print(" %18.8f Total Asks (Waves)" % grandtotal_asks_waves)
print(" %18.8f Average Ask (Waves)" % (grandtotal_asks_btc / grandtotal_asks_waves))
print
print("-" * 200)