from ast import Bytes
from datetime import datetime
from dataclasses import dataclass, field
from io import BytesIO


@dataclass
class Stock():
    ticker: str
    price: float
    change: float
    percentChange: float
    time: datetime
    logo: BytesIO = field(init=True, default=None)

    def update(self, price: float, change: float, percentChange: float,
               time: datetime):
        self.price = price
        self.change = change
        self.percentChange = percentChange
        self.time = time

    def addLogo(self, logo: BytesIO):
        self.logo = logo

    def __str__(self):
        if self.change > 0:
            return f"{self.time}: {self.ticker} {self.price:.2f} ^^^ {self.change:.2f}({self.percentChange:.2f}%)"
        elif self.change < 0:
            return f"{self.time}: {self.ticker} {self.price:.2f} ~~~ {self.change:.2f}({self.percentChange:.2f}%)"