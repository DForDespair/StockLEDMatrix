from abc import ABC, abstractmethod, abstractproperty
import json
import os
import requests
import exceptions as ex


class IIEXDataReceiver(ABC):
    """Creates interface for receiving data
    """

    @abstractmethod
    def fetch(self) -> json:
        pass

    @abstractmethod
    def add_tickers(self, tickers: list(str)) -> None:
        pass

    @abstractmethod
    def get_tickers(self) -> list(str):
        pass


class IEXStockReceiver(IIEXDataReceiver):
    """Gathers stock data from IEXCloud

    Args:
        IDataReceiver (_type_): _description_
    """
    _API_BASE = "https://cloud.iexapis.com/"
    _SANDBOX_BASE = "https://sandbox.iexapis.com"
    _TICKERS: list(str)
    _BATCHURL = _API_BASE + "stock/market/batch?symbols="

    def __init__(self, API_KEY=None, version="stable"):
        self._API_KEY = API_KEY or os.environ.get("API_KEY")
        if not self._API_KEY:
            raise ex.TokenNotFound("Token is not found")
        if version not in (["stable", "v1", "beta", "sandbox"]):
            raise ex.VersionNotFound(
                "Version must be one of following: stable, v1, sandbox or beta"
            )
        self._version = version

    def fetch(self) -> json:
        batch_request = self._API_BASE + self._BATCHURL.join([
            ticker + "," for ticker in self.get_tickers()
        ]) + "&types=quote?token=" + self._API_KEY
        if self._version == "sandbox":
            batch_request = self._SANDBOX_BASE + self._BATCHURL.join([
                ticker + "," for ticker in self.get_tickers()
            ]) + "&types=quote?token=" + self._API_KEY

        try:
            request = requests.get(batch_request)
            return json.loads(request)
        except requests.exceptions.Timeout:
            pass
        except requests.exceptions.TooManyRedirects:
            raise ex.TooManyRequests("Redirected too many times")
        except requests.exceptions.RequestException:
            pass

    def add_tickers(self, tickers) -> list(str):
        if len(tickers) <= 1:
            raise ex.NoSymbol("Not enough tickers. Please try more than 1")
        elif len(tickers) >= 100:
            raise ex.TooManyTickers(
                "You have entered too many tickers. please enter between 1 and 100"
            )
        self._TICKERS = tickers

    @get_tickers.getter
    def get_tickers(self) -> list(str):
        return self._TICKERS


class IEXLogoReceiver(IIEXDataReceiver):

    _API_BASE = "https://cloud.iexapis.com/"
    _SANDBOX_BASE = "https://sandbox.iexapis.com"
    _TICKERS: list(str)

    def __init__(self, API_KEY=None, version="stable"):
        self._API_KEY = API_KEY or os.environ.get("API_KEY")
        if not self._API_KEY:
            raise ex.TokenNotFound("Token is not found")
        if version not in (["stable", "v1", "beta", "sandbox"]):
            raise ex.VersionNotFound(
                "Version must be one of following: stable, v1, sandbox or beta"
            )
        self._version = version

    @add_tickers.setter
    def add_tickers(self, tickers):
        if len(tickers) <= 1:
            raise ex.NoSymbol("Not enough tickers. Please try more than 1")
        elif len(tickers) >= 100:
            raise ex.TooManyTickers(
                "You have entered too many tickers. please enter between 1 and 100"
            )
        self._TICKERS = tickers

    @get_tickers.getter
    def get_tickers(self):
        return self._TICKERS

    def fetch(self) -> json:
        batch_request = self._API_BASE + self._BATCHURL.join([
            ticker + "," for ticker in self.get_tickers()
        ]) + "&types=quote?token=" + self._API_KEY
        if self._version == "sandbox":
            batch_request = self._SANDBOX_BASE + self._BATCHURL.join([
                ticker + "," for ticker in self.get_tickers()
            ]) + "&types=quote?token=" + self._API_KEY
            try:
                request = requests.get(batch_request)
                return json.loads(request)
            except requests.exceptions.Timeout:
                pass
            except requests.exceptions.TooManyRedirects:
                raise ex.TooManyRequests("Redirected too many times")
            except requests.exceptions.RequestException:
                pass


class IEXDataFactory():

    def get_data(self, type):
        pass