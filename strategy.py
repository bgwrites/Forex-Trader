# Strategy logic & indicators go here
class strategyLogic():
    def SMA(self, prices, length, period):
        return sum(prices[(length-period):length]) / period

    def SMAprev(self, prices, length, period):
        return sum(prices[(length-period-1):length-1]) / period
