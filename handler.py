from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
import json
from traceback import print_tb
from PIL import Image
from io import BytesIO
import os

from cache import LogoCache, StockCache


class Handler(ABC):
    """Handler interface for IEX Data

    Args:
        ABC (Object): Abstract base clase
    """

    @abstractmethod
    def add(self):
        pass

    @abstractmethod
    def getCache(self):
        pass


class LogoDataHandler(Handler):
    """ Handles logo request from IEX Cloud and manages LogoCache and 

    Args:
        Handler (Object): Interface for IEX Data 
    """

    def __init__(self, directory: str, tickers: list):
        self.directory = directory
        self.logos = LogoCache()
        self.tickers = tickers

    def getCache(self) -> dict:
        return self.logos.get_logos()

    def add(self, ticker, image: Image) -> None:
        if self.logos.tryGet(ticker) == False:
            self.logos.add(ticker, image)

    def addToImageFolder(self, ticker: str, image: Image, filename: str,
                         directory: str):
        if self.logos.tryGet(ticker) == False:
            image.save(directory + '\\' + filename)

    def getDefaultImage(self) -> Image:
        if self.logos.tryGet('default'):
            return self.getCache()['default']

    def readLogoRequest(self, logorequest: dict, directory: str):
        for ticker in self.tickers:
            if ticker not in logorequest.keys():
                if self.logos.tryGet(ticker) == False:
                    print(
                        f'{ticker} logo not available. Setting default image...'
                    )
                    self.add(ticker, self.getDefaultImage())
            else:
                image = logorequest[ticker]
                filename = f"{ticker}.bmp"
                if ticker not in self.getCache().keys():
                    print(f'Adding {ticker} logo to image directory...')
                    self.addToImageFolder(ticker, image, filename,
                                          self.directory)
                    print(f'Adding {ticker} logo to cache...')
                    self.add(ticker, image)

    def get(self, ticker):
        if self.logos.tryGet(ticker):
            return self.getCache()[ticker]

    def addExistingLogos(self, directory: str):
        for file in os.listdir(directory):
            ticker = file.split(".")[0]
            image = Image.open(directory + "\\" + file)
            self.add(
                ticker,
                image,
            )


class StockDataHandler(Handler):

    def __init__(self):
        self.stocks = StockCache()

    def add(self, ticker, price: float, change: float, percentChange: float,
            timestamp: datetime):
        if self.stocks.tryGet(ticker):
            stock = self.stocks.get_stocks()[ticker]
            print(f"{timestamp}: Updating {ticker} in cache...")
            self.stocks.update(price, change, percentChange, stock, timestamp)
        else:
            print(f"{timestamp}: Adding {ticker} to cache...")
            self.stocks.add(ticker, price, change, percentChange, timestamp)

    def read_quote(self, stockQuote: dict) -> None:
        for ticker, quote in stockQuote.items():
            price = quote['quote']['latestPrice']
            change = quote['quote']['change']
            percentChange = quote['quote']['changePercent'] * 100
            timestamp = datetime.fromtimestamp(
                float(quote['quote']['latestUpdate']) / 1000)
            self.add(ticker, price, change, percentChange, timestamp)

    def getCache(self):
        return self.stocks.get_stocks()
