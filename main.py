import requests
from datetime import date, timedelta
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla"
STOCK_API_KEY = "key"
NEWS_API_KEY = "key"

account_sid = "sid"
auth_token = "token"
client = Client(account_sid,auth_token)


stockparameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY,
    "outputsize": "compact",
}

stockresponse = requests.get("https://www.alphavantage.co/query",params=stockparameters)
stockresponse.raise_for_status()
stockdata = stockresponse.json()
today_date = date.today()
yesterday = str(today_date - timedelta(1))
twodaysago = str(today_date - timedelta(2))
yesterday_values = stockdata["Time Series (Daily)"][f"{yesterday}"]
twodaysago_values = stockdata["Time Series (Daily)"][f"{twodaysago}"]

yesterday_open = float(yesterday_values["1. open"])
twodaysago_open = float(twodaysago_values["1. open"])
posorneg = yesterday_open-twodaysago_open
daily_change = abs(yesterday_open-twodaysago_open)/yesterday_open


# This if statement needs to be turned on to test when api calls are available again
if daily_change > 0.05:
    newsparameters = {
        "q": COMPANY_NAME,
        "apikey": NEWS_API_KEY,
    }
    newsresponse = requests.get("https://newsapi.org/v2/everything",params=newsparameters)
    newsresponse.raise_for_status()
    newsdata = newsresponse.json()
    print(newsdata)
    for index in range(1,4):
        news_headline = newsdata["articles"][index]["title"]
        news_brief = newsdata["articles"][index]["description"]
        if posorneg > 0:
            message = client.messages.create(
                body=f"{STOCK}: 🔺{daily_change*100}%\nHeadline: {news_headline}.\nBrief: {news_brief}",
                from_= "phone number",
                to="phone number"
            )
        else:
            message = client.messages.create(
                body=f"{STOCK}: 🔻{daily_change*100}%\nHeadline: {news_headline}.\nBrief: {news_brief}",
                from_= "phone number",
                to="phone number"
            )





