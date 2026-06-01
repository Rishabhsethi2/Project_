import yaml, os
from exceptions import TradingPlatformException

class AppConfig():
    _instance = None

    MARKET_OPEN_TIME="09:15"
    MARKET_CLOSE_TIME="15:30"
    STOCK_LIST=["Reliance","Adani"]
    
    def __new__(cls,*args,**kwargs):
        if cls._instance is None:
            cls._instance=super().__new__(cls)
        return cls._instance
    
    def __init__(cls):

        try:
            with open('settings.yaml','r') as f:
                data = yaml.safe_load(f)
                if data is None:
                    raise TradingPlatformException("No data in YAML file!!")
            for key,value in data.items():
                setattr(AppConfig, key, value)
        except TradingPlatformException as e:
            print(e)
        except yaml.YAMLError as e:
            print(f"YAML syntax error occured: {e}")
        except Exception as e:
            print(f"Unexpected error occured: {e}")

eg = AppConfig()

print(AppConfig.MARKET_CLOSE_TIME)
print(AppConfig.MARKET_OPEN_TIME)
print(AppConfig.trading)
print(AppConfig.network)