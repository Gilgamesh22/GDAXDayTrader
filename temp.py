# Set a default product
PC = GDAX.PublicClient(api_url="https://api.gdax.com", product_id="ETH-USD")
#print(json.dumps(PC.getProducts(), sort_keys=True, indent=4))
#print(json.dumps(PC.getProductOrderBook(), sort_keys=True, indent=4))
#print(json.dumps(PC.getProductTicker(), sort_keys=True, indent=4))
#print(json.dumps(PC.getProductTrades(), sort_keys=True, indent=4))
#print(json.dumps(PC.getProductHistoricRates(granularity=1000 , start='2017-05-04', end='2017-05-05' ), sort_keys=True, indent=4))