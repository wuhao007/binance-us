import requests
import urllib.parse
import hashlib
import hmac
import base64
import time

class BinanceUs:

    def __init__(self): 
        self.api_url = 'https://api.binance.us'
        self.api_key = ''
        self.secret_key = ''

    # get binanceus signature 
    def get_binanceus_signature(self, data):
        postdata = urllib.parse.urlencode(data)
        message = postdata.encode()
        byte_key = bytes(self.secret_key, 'UTF-8')
        mac = hmac.new(byte_key, message, hashlib.sha256).hexdigest()
        return mac

    # Attaches auth headers and returns results of a POST request
    def binanceus_request(self, uri_path, data):
        headers = {}
        headers['X-MBX-APIKEY'] = self.api_key
        signature = self.get_binanceus_signature(data)
        params={
            **data,
            "signature": signature,
            }          
        req = requests.get((self.api_url + uri_path), params=params, headers=headers)
        return req.text

    def TestConnectivity(self):
        resp = requests.get(self.api_url + '/api/v3/ping')
        return resp.json()

    def GetServerTime(self):
        resp = requests.get(self.api_url + '/api/v3/time')
        return resp.json()

    def GetSystemStatus(self):
        uri_path = "/sapi/v1/system/status"
        data = {
           "timestamp": int(round(time.time() * 1000)),
        }

        result = self.binanceus_request(uri_path, data)
        print("GET {}: {}".format(uri_path, result))
        return result

    def GetExchangeInformation(self):
        resp = requests.get(self.api_url + '/api/v3/exchangeInfo')
        return resp.json()

    def GetRecentTrades(self, symbol):
        resp = requests.get(self.api_url + f'/api/v3/trades?symbol={symbol}')
        return resp.json()

    def GetHistoricalTrades(self, symbol):
        headers = {}
        headers['X-MBX-APIKEY'] = self.api_key
        resp = requests.get(self.api_url + f'/api/v3/historicalTrades?symbol={symbol}', headers=headers)
        return resp.json()

    def GetAggregateTrades(self, symbol):
        resp = requests.get(self.api_url + f'/api/v3/aggTrades?symbol={symbol}')
        return resp.json()


def main():
    binance_us = BinanceUs()
    print(binance_us.TestConnectivity())
    print(binance_us.GetServerTime())
    print(binance_us.GetSystemStatus())
    # print(binance_us.GetExchangeInformation())
    # print(binance_us.GetRecentTrades('BTCUSD'))
    # print(binance_us.GetHistoricalTrades('BTCUSD'))
    print(binance_us.GetAggregateTrades('BTCUSD'))


if __name__ == '__main__':
    main()
