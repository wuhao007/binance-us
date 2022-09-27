import unittest
import binance_us


class TestBinanceUs(unittest.TestCase):

    def setUp(self):
        self.binance_us = binance_us.BinanceUs()

    def test_connectivity(self):
        self.assertEqual(self.binance_us.TestConnectivity(), {})

    def test_server_time(self):
        self.assertEqual(self.binance_us.GetServerTime().get('serverTime') > 1664300791770, True)

    def test_get_system_status(self):
        self.assertEqual(self.binance_us.GetSystemStatus(), '{"status":0}')
