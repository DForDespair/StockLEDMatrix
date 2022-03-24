from ensurepip import version
import unittest
import iexcloud


class TestIEXFactory(unittest.TestCase):

    def test_creates_iex_stock_receivers(self):
        tickers = ['aapl']
        api_key = ""
        stock = iexcloud.IEXDataFactory.stock_receiver(tickers,
                                                       api_key,
                                                       version='stable')
        self.assertIsInstance(
            iexcloud.IEXStockReceiver(tickers, api_key, "stable"), stock)


if __name__ == "__main__":
    unittest.main()