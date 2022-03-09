from abc import ABC, abstractmethod
import json


class IDataReceiver(ABC):
    """Creates interface for receiving data
    """
    @abstractmethod
    def fetch(self) -> json:
        pass
    
    
class IEXCloudReceiver(IDataReceiver):
    """Gathers stock data from IEXCloud

    Args:
        IDataReceiver (_type_): _description_
    """
    
    def generate_connection
    def __init__(self, _API_KEY):
        self.API_KEY = _API_KEY
    def fetch(self) -> json:
        pass 


class MarketWatchReceiver():
    
    def fetch(self) -> json:
        pass 
        