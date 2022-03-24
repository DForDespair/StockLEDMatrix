from abc import ABC, abstractmethod
from datetime import datetime
from io import BytesIO
from xmlrpc.client import boolean
from stock import Stock
from dataclasses import dataclass, field
from PIL import Image


class ICache(ABC):

    @abstractmethod
    def add(self):
        pass

    @abstractmethod
    def tryGet(self):
        pass


@dataclass
class StockCache(ICache):
    stocks: dict = field(default_factory=dict)

    def add(self, ticker: str, price: float, change: float,
            percentChange: float, time: datetime) -> None:
        stock = Stock(ticker, price, change, percentChange, time)
        self.stocks[stock.ticker] = stock

    def tryGet(self, ticker: str) -> boolean:
        stock = True if ticker in self.stocks.keys() else False
        return stock

    def update(self, price: float, change: float, percentChange: float,
               stock: Stock, time: datetime) -> None:
        stock.update(price, change, percentChange, time)

    def print_stocks(self) -> None:
        for stock in self.stocks.values():
            print(stock)

    def get_stocks(self) -> dict:
        return self.stocks


@dataclass
class LogoCache(ICache):
    logos: dict = field(default_factory=dict)

    def add(self, ticker: str, logo: Image):
        self.logos[ticker] = logo

    def tryGet(self, ticker: str) -> boolean:
        logo = True if ticker in self.logos.keys() else False
        return logo

    def get_logos(self) -> dict:
        return self.logos
