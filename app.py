from strategy import strategyLogic
from candles import candleLogic
from __init__ import userVals

# Oanda Packages
from oandapyV20 import API
import oandapyV20
from oandapyV20.contrib.requests import MarketOrderRequest
from oandapyV20.contrib.requests import TakeProfitDetails, StopLossDetails
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.accounts as accounts

class trading():
    # state management
    def __init__(self):
      self.resistance = 0
      self.support = 0
      self.status = "Not Trading"
      self.currentTrade = ""
      self.kill = False # <----- This is a kill switch. If it is true, the bot will shut down.

      #initialize data channel
      s = strategyLogic()  
      c = candleLogic()
      self.data = c.getData()         

      #Initialize Indicators
      self.currentClose = self.data[-1]
      self.lotSize = ()
      self.SMA1 = s.SMA(self.data, userVals.count, userVals.SMAbig)
      self.SMA1previous = s.SMAprev(self.data, userVals.count, userVals.SMAbig)
      self.SMA2 = s.SMA(self.data, userVals.count, userVals.SMAsmall)
      self.SMA2previous = s.SMAprev(self.data, userVals.count, userVals.SMAsmall)      

    # Entry/Exit confirmations
    def enterLong(self):
      if (self.SMA1 < self.SMA2) and (self.SMA1previous < self.SMA2): return True
      return False

    def enterShort(self): 
      if (self.SMA1 > self.SMA2) and (self.SMA1previous > self.SMA2): return True 
      return False

    # Check account for open trades
    def getTrades(self):
      r = accounts.AccountDetails(userVals.accountID)
      client = API(access_token=userVals.key)
      rv = client.request(r)
      self.details = rv.get('account')
      return self.details.get('openTradeCount')

    # Calculate lot size depending on risk %
    def lots(self):
      r = accounts.AccountDetails(userVals.accountID)
      client = API(access_token=userVals.key)
      rv = client.request(r)
      self.details = rv.get('account')      
      balance = self.details.get('NAV')
      size = 0
      # different calculation based on trade type
      if self.enterLong() == True:
        size = abs(int((float(balance) * float(userVals.risk)) / (self.currentClose - self.support)))
      elif self.enterShort() == True:
        size = abs(int((float(balance) * float(userVals.risk)) / (self.currentClose - self.resistance)))
      return size

    #Define closeout
    def closePosition(self):
      if self.currentTrade == "Long":
        data = {"longUnits": "ALL"}
        client = oandapyV20.API(access_token=userVals.key)
        r =positions.PositionClose(accountID=userVals.accountID, instrument=userVals.instrument, data=data)
        client.request(r)
      elif self.currentTrade == "Long":
        data = {"shortUnits": "ALL"}
        client = oandapyV20.API(access_token=userVals.key)
        r =positions.PositionClose(accountID=userVals.accountID, instrument=userVals.instrument, data=data)
        client.request(r)      

    # main trading function
    def main(self):
      self.resistance = max(self.data[(userVals.count-6):userVals.count])
      self.support = min(self.data[(userVals.count-6):userVals.count])

      # Oanda Parameters
      mktOrderLong = MarketOrderRequest(instrument=userVals.pair,
                      units= self.lots(),
                      takeProfitOnFill=TakeProfitDetails(price=self.resistance).data,
                      stopLossOnFill=StopLossDetails(price=self.support).data)
      mktOrderShort = MarketOrderRequest(instrument=userVals.pair,
                       units= (self.lots() *-1),
                       takeProfitOnFill=TakeProfitDetails(price=self.support).data,
                       stopLossOnFill=StopLossDetails(price=self.resistance).data)

      # Trading Conditions
      if self.getTrades() == 0:
        print "Looking for trades."
        if self.enterLong() == True:
           api = oandapyV20.API(access_token=userVals.key)
           r = orders.OrderCreate(userVals.accountID, data=mktOrderLong.data)
           api.request(r)
           self.status == "Trading"
           self.currentTrade == "Long"
           print "Trade Executed"

        elif self.enterShort() == True:
           api = oandapyV20.API(access_token=userVals.key)
           r = orders.OrderCreate(userVals.accountID, data=mktOrderShort.data)
           api.request(r)
           self.status == "Trading"
           self.currentTrade == "Short"
           print "Trade Executed"

        elif self.enterLong() and self.enterShort() == False:
           print "No Trades Open, Looking for Entry..."
      else:
        if self.currentTrade == "Short":
          if self.enterLong() == True:
             self.closePosition()
             self.status == "Not Trading"
             print "Trade Exited"
          else:
            print "No exits.. Looking"
        elif self.currentTrade == "Long":
          if self.enterShort() == True:
             self.closePosition()
             self.status == "Not Trading"
             print "Trade Exited"
          else:
            print "No exits.. Looking"
        else:
            self.kill = True
            print "Error, Closing down."

# Run the bot and kill it if kill switch is engaged
if __name__ == "__main__":
  t = trading()
  while(t.kill == False):
    t.main()
