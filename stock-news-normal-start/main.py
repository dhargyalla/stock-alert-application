import requests
import os
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
MY_API_KEY = "your api key"
MY_NEWS_API_KEY = "news api key"

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']

    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

#Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]

parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": MY_API_KEY,
}
response = requests.get(STOCK_ENDPOINT, params=parameters)
data = response.json()
day_closing = data['Time Series (Daily)']
closing_stock_price = [value for (key, value) in day_closing.items()]
yesterday_closing = float(closing_stock_price[0]['4. close'])

# Get the day before yesterday's closing stock price
day_before_yesterday_closing = float(closing_stock_price[1]['4. close'])

# Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
difference = yesterday_closing - day_before_yesterday_closing
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

# Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.

percentage = round((difference / day_before_yesterday_closing) * 100)

# If TODO4 percentage is greater than 5 then print("Get News").

news_parameters = {
    "qInTitle": COMPANY_NAME,
    "apiKey": MY_NEWS_API_KEY,
}

response = requests.get(NEWS_ENDPOINT, params=news_parameters)
data_news = response.json()
tesla_news = data_news['articles']

    ## STEP 2: https://newsapi.org/ 
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

#Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.
if abs(percentage) > 1:
    url_news = "https://newsapi.org/v2/everything"
    news_parameters = {
        "q":STOCK_NAME,
        "from": "2024-08-17",
        "sortBy": COMPANY_NAME,
        "apiKey":MY_NEWS_API_KEY,
    }

    response = requests.get(url_news, params=news_parameters)
    data_news = response.json()
#TODO 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
    first_three = data_news['articles'][:3]


    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number. 

# Create a new list of the first 3 article's headline and description using list comprehension.
    formated_articles = required_articles = [f"{STOCK_NAME}: {up_down}{percentage}% \n Headline: {item['title']}. \n Brief: {item['description']}" for item in first_three]

#Send each article as a separate message via Twilio.
    client = Client(account_sid, auth_token)
    for article in formated_articles:
        message = client.messages.create(
            body=article,
            from_='+1*****2661',
            to='+1********310'
        )

#Optional TODO: Format the message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

