import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

TASLA_API = "F47KWWFB104ID35D"
NEWS_API = "121c49d5bd67409aa38d515e40be391d"
TWILIO_SID = "Your SID"
TWLIO_AUTH = "Your AUTH"

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": TASLA_API,
}


response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing = yesterday_data["4. close"]
print(yesterday_closing)

before_yesterday_data = data_list[1]
before_yesterday_closing = before_yesterday_data["4. close"]
print(before_yesterday_closing)

difference = abs(float(yesterday_closing) - float(before_yesterday_closing))
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"
print(difference)

diff_percent = round((difference / float(yesterday_closing)) * 100)
print(diff_percent)

if diff_percent > 2:
    news_params = {
    "q": COMPANY_NAME,
    "sortBy": "popularity&",
    "apikey": NEWS_API,
    }

    response = requests.get(NEWS_ENDPOINT, news_params)
    articles = response.json()["articles"]
    three_articles = articles[:3]
    formated_articles = [f"{STOCK_NAME}: {up_down} {diff_percent}% \nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
    print(formated_articles)

    client = Client(TWILIO_SID, TWLIO_AUTH)
    for article in formated_articles:
        message = client.messages.create(
            body=article,
            from_="TRIAL NUMBER",
            to= "your number"
        )