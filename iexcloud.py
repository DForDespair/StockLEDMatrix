from abc import ABC, abstractmethod
from audioop import add
from datetime import datetime
from io import BytesIO
import json
import os
import requests
from cache import StockCache
import exceptions as ex
from filehandler import LogoHandler
from PIL import Image

from stock import Stock


class IIEXDataReceiver(ABC):
    """Creates interface for receiving data
    """

    @abstractmethod
    def fetch(self) -> json:
        pass


class IEXStockReceiver(IIEXDataReceiver):
    """Gathers stock data from IEXCloud

    Args:
        IDataReceiver (_type_): _description_
    """
    _API_BASE = "https://cloud.iexapis.com"
    _SANDBOX_BASE = "https://sandbox.iexapis.com"
    _TICKERS: list
    _BATCHURL = "stock/market/batch?symbols="

    def __init__(self, tickers: list, API_KEY, version="sandbox"):
        self._API_KEY = API_KEY
        if version not in (["stable", "v1", "beta", "sandbox"]):
            raise ex.VersionNotFound(
                "Version must be one of following: stable, v1, sandbox or beta"
            )
        self._version = version
        self._TICKERS = tickers

    def fetch(self) -> json:
        sep_tickers = ",".join([ticker for ticker in self._TICKERS])
        batch_request = f"{self._API_BASE}/{self._version}/{self._BATCHURL}{sep_tickers}&types=quote&token={self._API_KEY}"
        if self._version == "sandbox":
            batch_request = f"{self._SANDBOX_BASE}/stable/{self._BATCHURL}{sep_tickers}&types=quote&token={self._API_KEY}"
        try:
            print('Receiving quotes')
            request = requests.get(batch_request)
            request.raise_for_status()
            return request.json()
        except requests.exceptions.HTTPError:
            raise ex.NotFound("Not found")


class IEXLogoReceiver(IIEXDataReceiver):

    def __init__(self, tickers: list):
        self._TICKERS = tickers
        self.logo_names = [x.split(".")[0] for x in os.listdir("./images")]

    def fetch(self):
        base_url = "https://storage.googleapis.com/iex/api/logos/"

        for ticker in self._TICKERS:
            try:

                print('Receiving image.')
                request = requests.get(base_url + ticker + ".png", stream=True)
                request.raise_for_status()
                filename = ("./images/" + ticker + '.bmp')
                image = Image.open(BytesIO(request.content))
                image.save(filename)
            except requests.exceptions.HTTPError as e:
                continue


class IEXDataFactory():

    def stock_receiver(self, tickers, API_KEY, version) -> IIEXDataReceiver:
        return IEXStockReceiver(tickers, API_KEY, version)

    def logo_receiver(self, tickers) -> IIEXDataReceiver:
        return IEXLogoReceiver(tickers, )


class StockDataHandler():

    def __init__(self):
        self.stocks = StockCache()

    def read_quote(self, stockQuote: json) -> None:
        for ticker, quote in stockQuote.items():
            price = quote['quote']['iexRealtimePrice']
            change = quote['quote']['change']
            percentChange = quote['quote']['changePercent'] * 100
            timestamp = datetime.fromtimestamp(
                float(quote['quote']['iexLastUpdated']) / 1000)
            if self.stocks.tryGet(ticker):
                stock = self.stocks.get_stocks()[ticker]
                self.stocks.update(price, change, percentChange, stock,
                                   timestamp)
            else:
                self.stocks.add(ticker, price, change, percentChange,
                                timestamp)
