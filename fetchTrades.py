import ccxt
import time
#print(ccxt.phemex)

#Get exchange info and authenticate
exchange = ccxt.phemex({
    'enableRateLimit': True,  # https://github.com/ccxt/ccxt/wiki/Manual#rate-limit
    'apiKey': '7ca49559-1bcd-426b-88f9-abb26db5872e',  # testnet keys if using the testnet sandbox
    'secret': 'WQPItpDitbveNBVKOMbhY6n1YetcUgOsu3JKCqpU9NVjZDNkNzY1Mi03NDczLTRhYmYtOTU1NC1iZmMyMTQ2NjEyZGI',  # testnet keys if using the testnet sandbox
    'options': {
        'defaultType': 'swap',
    },
})

#Set TestNet
exchange.set_sandbox_mode(True)
markets = exchange.load_markets()

trades = exchange.fetch_my_trades('BTC/USD',None, 5)

print(trades[4])

balance = exchange.fetch_balance({'code':'BTC'})

print(balance)
