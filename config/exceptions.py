class TradingPlatformException(Exception):

    def __init__(self,message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"TradingPlatformException: {self.message}."
    
class NetworkTimeoutException(TradingPlatformException):
    def __init__(self,message="Network timed out"):
        super().__init__(message)
    


def handle_system_error(func):
    def wrapper(*args,**kwargs):
        try:
            return func(*args,**kwargs)
        except NetworkTimeoutException:
            print("[ERROR] Network timeout detected. Initiating circuit breaker protocols...")
    return wrapper

#tests
# @handle_system_error
# def risky_op():
#     raise NetworkTimeoutException()
# risky_op()
