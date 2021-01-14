import ccxt
#print(ccxt.phemex)

exchange = ccxt.phemex({
    'enableRateLimit': True,  # https://github.com/ccxt/ccxt/wiki/Manual#rate-limit
    'apiKey': '7ca49559-1bcd-426b-88f9-abb26db5872e',  # testnet keys if using the testnet sandbox
    'secret': 'WQPItpDitbveNBVKOMbhY6n1YetcUgOsu3JKCqpU9NVjZDNkNzY1Mi03NDczLTRhYmYtOTU1NC1iZmMyMTQ2NjEyZGI',  # testnet keys if using the testnet sandbox
    'options': {
        'defaultType': 'swap',
    },
})

# exchange.set_sandbox_mode(True)  # uncomment to use the testnet sandbox

exchange.set_sandbox_mode(True)
markets = exchange.load_markets()

positions = exchange.fetch_positions(None, None, None, {'code':'BTC'})
#print(positions)

balance = exchange.fetch_balance({'code':'BTC'})
print(balance)
