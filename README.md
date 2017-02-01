# Forex-Trader

This is the code for developing an automated Forex trading system using Oanda as a broker. I plan to implement many features into this, so if you have anything you want to see, fell free to leave comments under issues.

List of planned features:
  - Fibonacci retracement and extenson levels
  - RSI indicator
  - Multi time frame analysis.

# Getting started
<b>DISCLAIMER! Forex trading carries a heavy amount of risk. Any and everything outlined in this code is for educational purposes only. I am not responsible for any of your losses or any hardships you may face as a result of using this code. Again, this is meant to be used ONLY for educational purposes.</b>

You will need to install <a href="https://github.com/hootnot/oanda-api-v20">oandapyV20</a> and <a href="https://pypi.python.org/pypi/requests/">requests</a>

This strategy is based on a 2 simple moving average cross. The TP/SL levels are set with support and resistance lines for the past candles.

1. Create a demo account with <a href="https://oanda.com">Oanda</a> and obtain an api key and make note of your account ID.
2. Place your accountID and api key in their respective ares in the __init__.py file.
3. Within __init__.py place the numbers you want for your 2 Simple Moving Averages in "SMAbig" and "SMAsmall".
4. Depending on what your largest SMA is, you will need to set "count" to the same or more. I like to load in a few extra to alow for more data manipulation.
5. Point your terminal to the project directory and run app.py in terminal with:

> user$: python app.py

<b>Your system should now be running!</b>
