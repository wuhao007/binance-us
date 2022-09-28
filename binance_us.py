import requests
import urllib.parse
import hashlib
import hmac
import base64
import time

class BinanceUs:

    def __init__(self): 
        self.api_url = 'https://api.binance.us'

    # get binanceus signature 
    def get_binanceus_signature(self, data):
        postdata = urllib.parse.urlencode(data)
        message = postdata.encode()
        byte_key = bytes(self.secret_key, 'UTF-8')
        mac = hmac.new(byte_key, message, hashlib.sha256).hexdigest()
        return mac

    # Attaches auth headers and returns results of a POST request
    def binanceus_request(self, uri_path):
        headers = {}
        headers['X-MBX-APIKEY'] = self.api_key
        data = self.GetTimestamp()
        signature = self.get_binanceus_signature(data)
        params={
            **data,
            "signature": signature,
            }          
        req = requests.get((self.api_url + uri_path), params=params, headers=headers)
        self.GetResult(uri_path, req.text)
        return req.text

    def request(self, endpoint, headers={}):
        resp = requests.get(self.api_url + '/api/v3/' + endpoint, headers=headers)
        return resp.json()

    def TestConnectivity(self):
        return self.request('ping')

    def GetServerTime(self):
        return request('time')

    def GetTimestamp(self):
        return {
           "timestamp": int(round(time.time() * 1000)),
        }

    def GetResult(self, uri_path, result):
        print("GET {}: {}".format(uri_path, result))

    def GetExchangeInformation(self):
        return request('exchangeInfo')

    def GetRecentTrades(self, symbol):
        return request(f'trades?symbol={symbol}')

    def GetHistoricalTrades(self, symbol):
        return request(f'historicalTrades?symbol={symbol}', {'X-MBX-APIKEY': self.api_key})

    def GetAggregateTrades(self, symbol):
        return request(f'aggTrades?symbol={symbol}')

    def GetOrderBookDepth(self, symbol):
        return request(f'depth?symbol={symbol}')

    def GetCandlestickData(self, symbol, interval):
        return request(f'klines?symbol={symbol}&interval={interval}')

    def AddSymbol(self, symbol):
        return f'?symbol={symbol}' if symbol else ''

    def GetLiveTickerPrice(self, symbol=None):
        return request('ticker/price' + self.AddSymbol(symbol))

    def GetAveragePrice(self, symbol):
        return request(f'avgPrice?symbol={symbol}')

    def GetBestOrderBookPrice(self, symbol=None):
        return request('ticker/bookTicker' + self.AddSymbol(symbol))

    def Get24hPriceChangeStatistics(self, symbol=None):
        return request('ticker/24hr' + self.AddSymbol(symbol))

    def GetRollingWindowPriceChangeStatistics(self, symbol=None):
        return request('ticker' + self.AddSymbol(symbol))
    
    def GetSystemStatus(self):
        return self.binanceus_request("/sapi/v1/system/status")

    def GetUserAccountInformation(self):
        return self.binanceus_request("/api/v3/account")

    def GetUserAccountStatus(self):
        return self.binanceus_request("/sapi/v3/accountStatus")

    def GetUserAPITradingStatus(self):
        return self.binanceus_request("/sapi/v3/apiTradingStatus")


def main():
    binance_us = BinanceUs()
    # print(binance_us.TestConnectivity())
    # print(binance_us.GetServerTime())
    print(binance_us.GetSystemStatus())
    # print(binance_us.GetExchangeInformation())
    # print(binance_us.GetRecentTrades('BTCUSD'))
    # print(binance_us.GetHistoricalTrades('BTCUSD'))
    # print(binance_us.GetAggregateTrades('BTCUSD'))
    # print(binance_us.GetOrderBookDepth('BTCUSD'))
    # print(binance_us.GetCandlestickData('BTCUSD', '1m'))
    # print(binance_us.GetLiveTickerPrice('BTCUSD'))
    # print(binance_us.GetAveragePrice('BTCUSD'))
    # print(binance_us.GetBestOrderBookPrice('BTCUSD'))
    # print(binance_us.Get24hPriceChangeStatistics('BTCUSD'))
    # print(binance_us.GetRollingWindowPriceChangeStatistics('BTCUSD'))
    # print(binance_us.GetUserAccountInformation)
    print(binance_us.GetUserAccountStatus())
    print(binance_us.GetUserAPITradingStatus())


if __name__ == '__main__':
    main()
