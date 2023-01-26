import requests
import urllib.parse
import hashlib
import hmac
import base64
import time
import sys

class BinanceUs:

    def __init__(self): 
        self.api_url = 'https://api.binance.us'
        self.headers = {}
        self.headers['X-MBX-APIKEY'] = self.api_key

    # get binanceus signature 
    def get_binanceus_signature(self, data):
        postdata = urllib.parse.urlencode(data)
        message = postdata.encode()
        byte_key = bytes(self.secret_key, 'UTF-8')
        mac = hmac.new(byte_key, message, hashlib.sha256).hexdigest()
        return mac

    # Attaches auth headers and returns results of a POST request
    def GetData(self):
        return {"timestamp": int(round(time.time() * 1000))}

    # Attaches auth headers and returns results of a POST request
    def GetParams(self, data):
        signature = self.get_binanceus_signature(data)
        return {
            **data,
            "signature": signature,
        }          

    def binanceus_get_request(self, uri_path, snapshot_type=None, recv_window=None, order_id=None, symbol=None):
        data = self.GetData()
        if snapshot_type:
            data['type'] = snapshot_type
        if recv_window:
            data['recvWindow'] = recv_window
        if order_id:
            data['orderId'] = order_id
        if symbol:
            data['symbol'] = symbol
        params = self.GetParams(data)
        req = requests.get((self.api_url + uri_path), params=params, headers=self.headers)
        print("GET {}: {}".format(uri_path, req))
        return req.text

    def binanceus_post_request(self, uri_path, symbol=None, side=None, order_type=None, quantity=None, quote_order_qty=None):
        data = self.GetData()
        if symbol:
            data['symbol'] = symbol
        if side:
            data['side'] = side
        if order_type:
            data['type'] = order_type
        if quantity:
            data['quantity'] = quantity
        if quote_order_qty:
            data['quoteOrderQty'] = quote_order_qty
        params = self.GetParams(data)
        req = requests.post((self.api_url + uri_path), headers=self.headers, data=params)
        print("POST {}: {}".format(uri_path, req))
        return req.text

    def binanceus_delete_request(self, uri_path, symbol=None, order_id=None):
        data = self.GetData()
        if symbol:
            data['symbol'] = symbol
        if order_id:
            data['orderId'] = order_id
        params = self.GetParams(data)
        req = requests.delete((self.api_url + uri_path), params=params, headers=self.headers)
        print("DELETE {}: {}".format(uri_path, req))
        return req.text

    def request(self, endpoint, headers={}):
        resp = requests.get(self.api_url + '/api/v3/' + endpoint, headers=headers)
        return resp.json()

    def AddSymbol(self, symbol):
        return f'?symbol={symbol}' if symbol else ''

    def TestConnectivity(self):
        return self.request('ping')

    def GetServerTime(self):
        return self.request('time')

    def GetExchangeInformation(self):
        return self.request('exchangeInfo')

    def GetRecentTrades(self, symbol):
        return self.request(f'trades?symbol={symbol}')

    def GetHistoricalTrades(self, symbol):
        return self.request(f'historicalTrades?symbol={symbol}', {'X-MBX-APIKEY': self.api_key})

    def GetAggregateTrades(self, symbol):
        return self.request(f'aggTrades?symbol={symbol}')

    def GetOrderBookDepth(self, symbol):
        return self.request(f'depth?symbol={symbol}')

    def GetCandlestickData(self, symbol, interval):
        return self.request(f'klines?symbol={symbol}&interval={interval}')

    def GetLiveTickerPrice(self, symbol=None):
        return self.request('ticker/price' + self.AddSymbol(symbol))

    def GetAveragePrice(self, symbol):
        return self.request(f'avgPrice?symbol={symbol}')

    def GetBestOrderBookPrice(self, symbol=None):
        return self.request('ticker/bookTicker' + self.AddSymbol(symbol))

    def Get24hPriceChangeStatistics(self, symbol=None):
        return self.request('ticker/24hr' + self.AddSymbol(symbol))

    def GetRollingWindowPriceChangeStatistics(self, symbol=None):
        return self.request('ticker' + self.AddSymbol(symbol))
    
    def GetSystemStatus(self):
        return self.binanceus_get_request("/sapi/v1/system/status")

    def GetUserAccountInformation(self):
        return self.binanceus_get_request("/api/v3/account")

    def GetUserAccountStatus(self):
        return self.binanceus_get_request("/sapi/v3/accountStatus")

    def GetUserAPITradingStatus(self):
        return self.binanceus_get_request("/sapi/v3/apiTradingStatus")

    def GetAssetDistributionHistory(self):
        return self.binanceus_get_request("/sapi/v1/asset/assetDistributionHistory")

    def QuickDisableCryptoWithdrawal(self):
        return self.binanceus_post_request("/sapi/v1/account/quickDisableWithdrawal")

    def QuickEnableCryptoWithdrawal(self):
        return self.binanceus_post_request("/sapi/v1/account/quickEnableWithdrawal")

    def GetUsersSpotAssetSnapshot(self):
        return self.binanceus_get_request("/sapi/v1/accountSnapshot", snapshot_type='SPOT')

    def GetTradeFee(self):
        return self.binanceus_get_request('/sapi/v1/asset/query/trading-fee')

    def GetPast30daysTradeVolume(self):
        return self.binanceus_get_request('/sapi/v1/asset/query/trading-volume')

    def GetSubAccountInformation(self):
        return self.binanceus_get_request('/sapi/v3/sub-account/list')

    def GetOrderRateLimits(selfi, recv_window=None):
        return self.binanceus_get_request('/api/v3/rateLimit/order', recv_window=recv_window)

    def CreateNewOrder(self, symbol, side, order_type, quantity, quote_order_qty):
        return self.binanceus_post_request('/api/v3/order', symbol=symbol, side=side, order_type=order_type, quantity=quantity, quote_order_qty=quote_order_qty)

    def TestNewOrder(self, symbol, side, order_type, quantity, quote_order_qty):
        return self.binanceus_post_request('/api/v3/order/test', symbol=symbol, side=side, order_type=order_type, quantity=quantity, quote_order_qty=quote_order_qty)

    def GetOrder(self, symbol, order_id=None):
        return self.binanceus_get_request('/api/v3/order', symbol=symbol, order_id=order_id)

    def GetAllOpenOrders(self):
        return self.binanceus_get_request('/api/v3/openOrders')

    def CancelOrder(self, symbol, order_id=None):
        return self.binanceus_delete_request('/api/v3/order', symbol=symbol, order_id=order_id)

    def CancelOpenOrdersForSymbol(self, symbol):
        return self.binanceus_delete_request('/api/v3/openOrders', symbol=symbol)

    def GetTrades(self, symbol):
        return self.binanceus_get_request('/api/v3/myTrades', symbol=symbol)


def main():
    binance_us = BinanceUs()
    # print(binance_us.TestConnectivity())
    # print(binance_us.GetServerTime())
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
    # print(binance_us.GetSystemStatus())
    # print(binance_us.GetUserAccountInformation)
    # print(binance_us.GetUserAccountStatus())
    # print(binance_us.GetUserAPITradingStatus())
    # print(binance_us.GetAssetDistributionHistory())
    # print(binance_us.QuickDisableCryptoWithdrawal())
    # print(binance_us.QuickEnableCryptoWithdrawal())
    # print(binance_us.GetUsersSpotAssetSnapshot())
    # print(binance_us.GetTradeFee())
    # print(binance_us.GetPast30daysTradeVolume())
    # print(binance_us.GetOrderRateLimits())
    symbol, during = sys.argv[1], sys.argv[2]

    while True:
        # print(binance_us.CreateNewOrder())
        # print(binance_us.TestNewOrder('BTCUSD', 'BUY', 'MARKET', None, 10))
        print(binance_us.TestNewOrder(symbol, 'BUY', 'MARKET', None, 10))
        #sleep(11320.75472)
        time.sleep(float(during))
    # print(binance_us.GetOrder('BTCUSD'))
    # print(binance_us.GetAllOpenOrders())
    # print(binance_us.CancelOrder('BTCUSD'))
    # print(binance_us.CancelOpenOrdersForSymbol('BTCUSD'))
    # print(binance_us.GetTrades('BTCUSD'))



if __name__ == '__main__':
    main()
