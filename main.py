import sys
import requests
import json
import os
import iexcloud as iex
import time

if __name__ == "__main__":
    _API_KEY = "Tsk_0c13a792b3984153a0aa281086d284f9"
    tickers = ['aapl', 'intc', 'meta', 'chpt', 'curo', 'para']
    factory = iex.IEXDataFactory()

    stocks = factory.stock_receiver(tickers, _API_KEY, version="sandbox")
    logos = factory.logo_receiver(tickers=tickers)
    handler = iex.StockDataHandler()

    try:
        print("Press CTRL-C to stop.")
        while True:
            quote = stocks.fetch()
            handler.read_quote(quote)
            handler.stocks.print_stocks()
            time.sleep(10)
    except KeyboardInterrupt:
        sys.exit(0)
