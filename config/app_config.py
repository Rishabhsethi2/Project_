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
        pass
        