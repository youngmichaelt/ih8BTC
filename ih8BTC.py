import ccxt
import time
#print(ccxt.phemex)

#Get exchange info and authenticate
exchange = ccxt.phemex({
    'enableRateLimit': True,  # https://github.com/ccxt/ccxt/wiki/Manual#rate-limit
    'apiKey': '8fe7ab51-6634-4c7b-ac35-04eb6ef70e95',  # testnet keys if using the testnet sandbox
    'secret': 'ih1eLee49CBSCdDl4Od2E666P6PFWQpIXIHgkrwI7oZkNjQzYzNhMi0zM2UyLTRlZWMtYTBkZi0xZGI4MjgyZTRhYTY',  # testnet keys if using the testnet sandbox
    'options': {
        'defaultType': 'swap',
    },
})

#Set TestNet
exchange.set_sandbox_mode(True)
markets = exchange.load_markets()

#Get position data
positions = exchange.fetch_positions(None, None, None, {'code':'BTC'})
print("Current Positions: ")
print(positions)
print("\n")




balance = exchange.fetch_balance({'code':'BTC'})
print(f"Current Balance: {balance}")
print("\n")


side = positions[0]["side"]

##Check if position already open
if side == "None":
    openTrade = False
else:
    openTrade = True


print(f"Open Trade: {openTrade}\n")



params = {
    'stopLossEp': 38000,
    'stopPrice': 38000,
    'closeOnTrigger':True,
    'timeInForce': 'FillOrKill'
}
market = exchange.fetch_ticker('BTC/USD')['last']

#Open a trade
if openTrade == False:
    print(f"Creating Limit Sell Order for: {market}\n")
    print(exchange.create_order('BTC/USD','Limit','Sell',33400,market))
    openTrade = True
    

else:
    print("Position already open...\n")

    ##print(exchange.create_order('BTC/USD','Limit','Buy',10, market))

    #exchange.create_market_sell_order('BTC/USD',10)
    #exchange.create_limit_sell_order('BTC/USD',10, 40000)
    


i=0

#Main Loop

while i <= 15:

    #Get open positions
    positions = exchange.fetch_positions(None, None, None, {'code':'BTC'})

    #Get market price
    market = exchange.fetch_ticker('BTC/USD')['last']
    print(f"Market Price: {market}")

    

    #Check if order is waiting to be filled
    orders = exchange.fetch_open_orders('BTC/USD')

    #Check if position is open, get position price
    if openTrade == True and (positions[0]['size'] != 0) and len(orders) <= 0:

        #Calculate Unrealised PNL 
        markPrice = exchange.fetch_ticker('BTC/USD')['info']['markEp']/10000

        #Looks at market price, more cautious
        mp = exchange.fetch_ticker('BTC/USD')['last']

        posSize = positions[0]['size']
        contractSize = 1
        avgEntryPrice = positions[0]['avgEntryPrice']
        unRealizedPnl = ((posSize*contractSize) / mp - (posSize*contractSize) / avgEntryPrice)*mp
        entry = positions[0]["avgEntryPrice"]
        
        print(f"Position Price: {entry}")
        print(f"Position PNL: {unRealizedPnl}\n")

        #SELL... Check that position is open and market is above entry price
        if (unRealizedPnl < 0) and (openTrade == True) and (positions[0]['size'] != 0):
            print(f"Creating Limit Buy Order for: {market}\n")
            exchange.create_order('BTC/USD','Limit','Buy',positions[0]['size'], market+20)
            openTrade = False

        #TAKE PROFIT

        

    else:
        print("Position Not Open\n")

        if len(orders) > 0:
            print("Open order waiting to be filled\n")
        else:
            #BUY... Check that position is not open
            if (openTrade == False) and (positions[0]['size'] == 0 and len(orders) <=0):
                print(f"Creating Limit Sell Order for: {market}\n")
                exchange.create_order('BTC/USD','Limit','Sell',positions[0]['size'], market)
                openTrade = True

    
        
    
    time.sleep(10)

    #i += 1



#print(positions[0]["avgEntryPrice"])
##print(positions[0]['size'])
##    if positions[0]['size'] != 0:
##        print('open')
##print(exchange.cancel_all_orders('BTC/USD'))
##print(exchange.cancel_order('b31a88ec-be63-55bb-b80a-a293a4bf4e23', 'BTC/USD'))
##exchange.create_market_sell_order()

##print(exchange.create_order('BTC/USD','Market','Buy',10))


