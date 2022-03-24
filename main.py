import sys
from io import BytesIO
import os
from handler import StockDataHandler, LogoDataHandler
import iexcloud as iex
import time
from config import config

if __name__ == "__main__":
    _API_KEY = "Tsk_0c13a792b3984153a0aa281086d284f9"
    tickers = config['tickers']
    directory = r"C:\Users\amogh\Desktop\Coding\StockLEDMatrix\Assets\images"
    factory = iex.IEXDataFactory()

    stocks = factory.stock_receiver(tickers, _API_KEY, version="sandbox")
    logos = factory.logo_receiver(tickers=tickers)
    logo_request = logos.fetch()
    stockHandler = StockDataHandler()
    logoHandler = LogoDataHandler(directory, tickers)
    logoHandler.addExistingLogos(directory)
    logoHandler.readLogoRequest(logo_request, directory)
    try:
        print("Press CTRL-C to stop.")
        while True:
            quote = stocks.fetch()
            stockHandler.read_quote(quote)
            stockHandler.stocks.print_stocks()
            time.sleep(10)
    except KeyboardInterrupt:
        sys.exit(0)
