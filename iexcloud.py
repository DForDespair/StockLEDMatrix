from abc import ABC, abstractmethod
from audioop import add
from datetime import datetime
from io import BytesIO
import json
import os
import requests
from cache import StockCache
import exceptions as ex
from handler import LogoDataHandler
from PIL import Image

from stock import Stock


class IIEXDataReceiver(ABC):
    """Creates interface for receiving data
    """

    @abstractmethod
    def fetch(self) -> json:
        pass


class IEXStockReceiver(IIEXDataReceiver):
    """

    Raises:
        ex.VersionNotFound: _description_
        ex.NotFound: _description_

    Returns:
        JSON: returns a batch quote request from IEX Cloud in JSON format
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

    def fetch(self) -> dict:
        base_url = "https://storage.googleapis.com/iex/api/logos/"
        images = {}
        for ticker in self._TICKERS:
            try:
                print(f'Receiving image for {ticker}.')
                request = requests.get(base_url + ticker.upper() + ".png",
                                       stream=True)
                print(request.status_code)
                request.raise_for_status()
                if request.status_code == 200:
                    image = Image.open(BytesIO(request.content))
                    images[ticker] = image
            except requests.exceptions.HTTPError as e:
                print(f"{ticker} logo does not exist:")
                continue
        print(images)
        return images


class IEXDataFactory():

    def stock_receiver(self, tickers, API_KEY, version) -> IIEXDataReceiver:
        return IEXStockReceiver(tickers, API_KEY, version)

    def logo_receiver(self, tickers) -> IIEXDataReceiver:
        return IEXLogoReceiver(tickers)
