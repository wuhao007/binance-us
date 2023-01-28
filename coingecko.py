import math
import time
import json
import datetime
import requests
from sklearn.linear_model import LinearRegression
import numpy as np
from typing import Optional, Dict, Any, List, Tuple

_SECONDS_IN_A_DAY = 24 * 60 * 60 * 1000
_200_DAYS = 200
_START_DATE = {
    'bitcoin': '2009-01-03T00:00:00',
    'ethereum': '2014-06-01T00:00:00',
    'thorchain': '2019-07-20T00:00:00',
    'binancecoin': '2017-07-01T00:00:00',
    'matic-network': '2019-04-24T00:00:00',
    'chainlink': '2017-09-19T00:00:00',
    'ftx-token': '2019-05-08T00:00:00',
    'polkadot': '2017-10-14T00:00:00',
    'crypto-com-chain': '2017-05-18T00:00:00',
    'litecoin': '2013-04-27T00:00:00',
    'fantom': '2018-06-15T00:00:00',
    'basic-attention-token': '2017-05-31T00:00:00',
}
_API2COINGECKO = {
    'XXBTZUSD': 'bitcoin',
    'BTC/USD': 'bitcoin',
    'XETHZUSD': 'ethereum',
    'ETH/USD': 'ethereum',
    'MATICUSD': 'matic-network',
    'MATIC/USD': 'matic-network',
    'BTCUSD': 'bitcoin',
    'ETHUSD': 'ethereum',
}


class CoinGecko(object):

    def __init__(self, coin: str) -> None:
        self.coin = _API2COINGECKO[coin]
        self.start_date = _START_DATE[self.coin]

    def GetAvgHelper(self, items: np.array) -> float:
        return sum(1 / item[1] for item in items)

    def GetAvg(self) -> float:
        return _200_DAYS / self.GetAvgHelper(self.prices_200)

    def GetLogPrice(self) -> float:
        timestamp = self.prices_200[-1][0]
        return 10**(self.w * math.log(self.GetCoinDays(timestamp), 10) + self.b)

    def GetAns(self, ratio) -> float:
        a_ = self.GetAvgHelper(self.prices_200[-_200_DAYS + 1:])
        b_ = 1
        c_ = -_200_DAYS * self.GetLogPrice()
        return (-b_ + math.sqrt(b_**2 - 4 * a_ * c_ * ratio)) / (2 * a_)

    def Date2Timestamp(self) -> float:
        return datetime.datetime.timestamp(
            datetime.datetime.fromisoformat(self.start_date)) * 1000

    def Get200DaysPrices(self):
        self.prices_200 = self.prices[-_200_DAYS - 1:][:_200_DAYS]
        assert len(self.prices_200) == _200_DAYS, f'{_200_DAYS} items'

    def GetMarketChart(self, vs_currency: str) -> List[Tuple[float, float]]:
        resp = requests.get(
            f'https://api.coingecko.com/api/v3/coins/{self.coin}/market_chart?vs_currency={vs_currency}&days=max'
        )
        self.prices = np.array([price for price in resp.json()['prices'] if price[1]])

    def GetCoinDays(self, timestamp: float) -> float:
        return (timestamp - self.Date2Timestamp()) / _SECONDS_IN_A_DAY

    def GetWb(self) -> None:
        xdata = np.log10(self.GetCoinDays(self.prices[:, 0])).reshape(-1, 1)
        ydata = np.log10(self.prices[:, 1])

        reg = LinearRegression().fit(xdata, ydata)
        self.w, self.b = reg.coef_[0], reg.intercept_

        print(f'Score:\033[31m{reg.score(xdata, ydata)}\033[0m')
        print(f'w: {self.w}, b: {self.b}')

    def GetHaowu999(self) -> Tuple[float, float]:
        self.GetWb()

        ahr999 = self.GetAhr999()
        print(f'ahr999: {ahr999}')
        ratio = 1.2
        ahr999_120 = self.GetAns(ratio)
        print(f'ahr999={ratio}: {ahr999_120} USD')
        ratio = 0.45
        ahr999_045 = self.GetAns(ratio)
        print(f'ahr999={ratio}: {ahr999_045} USD')
        return ahr999, ahr999_120, ahr999_045

    def GetAhr999(self) -> float:
        end_item = self.prices_200[-1]
        return end_item[1]**2 / (self.GetAvg() * self.GetLogPrice())

    def GetPrices(self):
        self.GetMarketChart('usd')
        self.Get200DaysPrices()

    def add_own_data(self, opentm: float, price: float) -> None:
        self.prices = np.append(self.prices, [[opentm * 1000, price]], axis=0)
