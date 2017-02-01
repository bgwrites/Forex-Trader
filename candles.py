import requests as r
import numpy as np
from __init__ import userVals

from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments

class user1():
    client = API(access_token=userVals.key)
    o = instruments.InstrumentsCandles(instrument=userVals.pair,
    	params=userVals.params)

class candleLogic:
    def OHLC(self, data):
        # Call imported user1 class
        user1.client.request(user1.o)
        candles = user1.o.response.get("candles")
        candleData = candles[data].get("mid")

        # OHLC variables to return in array
        o = candleData.get("o")
        h = candleData.get("h")
        l = candleData.get("l")
        c = candleData.get("c")
        return float(o), float(h), float(l), float(c)

    # Define clean function routes for returning proper data
    def Open(self, data):
        return self.OHLC(data)[0]

    def High(self, data):
        return self.OHLC(data)[1]

    def Low(self, data):
        return self.OHLC(data)[2]

    def Close(self, data):
        return self.OHLC(data)[3]

    def getData(self):
        numList = []
        for x in range(0, userVals.count):
            numList.append(self.Close(x))
        return numList
