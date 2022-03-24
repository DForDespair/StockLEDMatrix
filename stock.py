from datetime import datetime
from dataclasses import dataclass, field
from io import BytesIO
import unicodedata
from PIL import Image


@dataclass
class Stock():
    """ Creates a stock object that holds the name and current price action of the stock

    Returns:
        Stock: a stock object
    """
    ticker: str
    price: float
    change: float
    percentChange: float
    time: datetime

    def update(self, price: float, change: float, percentChange: float,
               time: datetime):
        self.price = price
        self.change = change
        self.percentChange = percentChange
        self.time = time

    def __str__(self):
        up = u"\u2191"
        down = u"\u2193"
        if self.change > 0:
            return f"{self.time}: {self.ticker} {self.price:.2f} {up} {self.change:.2f}({self.percentChange:.2f}%)"
        elif self.change < 0:
            return f"{self.time}: {self.ticker} {self.price:.2f} {down} {self.change:.2f}({self.percentChange:.2f}%)"
        else:
            return f"{self.time}: {self.ticker} {self.price:.2f} = {self.change:.2f}({self.percentChange:.2f}%)"