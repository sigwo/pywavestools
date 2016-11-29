import requests
top50 = requests.get('https://bittrex.com/Api/v2.0/pub/currency/GetBalanceDistribution?currencyName=WAVES').json()['result']['Distribution']
print("-" * 25)
print(str.center("Top 50 Bittrex balances", 25))
print
print(" #             Balance")
print("-" * 25)
for i, bal in enumerate(top50):
    print("%2d     %18.8f" % (i + 1, bal['Balance']))
print("-" * 25)
   