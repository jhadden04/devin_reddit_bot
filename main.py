import praw
from heapq import nlargest
import requests
import bs4
from yahoo_fin import stock_info as si

# can easily scrape the price using
# https://finance.yahoo.com/quote/TSLA?p=TSLA&.tsrc=fin-srch. For this replace the TSLA with the correct ticker
reddit = praw.Reddit(client_id='0_w-HYtscWovfg',
                     client_secret='ZBUvGyUFWio8INkuHPL6Mrx06EIwOQ',
                     user_agent='a reddit instance',
                     username='TheBigBoyJohn123',
                     password='pogchamp')


def get_price(stock_ticker):
    """site = f"https://finance.yahoo.com/quote/{stock_ticker[:1]}?p={stock_ticker[:1]}&.tsrc=fin-srch"
    res = requests.get(site)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    soupy = soup.select('#srp-river-results > ul > li:nth-child(2) > div > div.s-item__info.clearfix > a')
    print(soupy[0].get_text())

    finnhub_client = finnhub.Client(api_key="c0ddkhv48v6sgrj2de20")
    res = finnhub_client.stock_candles(stock_ticker, 'D', 1590988249, 1591852249)
    print(res)"""
    return (si.get_live_price(stock_ticker))


numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, " ", ".", ";", ")", ",", "$", "?", ">", "<", "\"", "!"]
phrase = "$"
all_stocks = []
rankings = {}
stock_prices = {}
amount = {}
for comment in reddit.subreddit('wallstreetbets').stream.comments():
    if phrase in comment.body:
        index = comment.body.index(phrase)
        ticker = ""
        ticker += comment.body[index]
        x = 1
        try:

            if comment.body[index + x] in str(numbers):
                continue
        except:
            continue
        while True:
            try:

                if comment.body[index + x] not in numbers:
                    ticker += comment.body[index + x]
                    x += 1

                else:
                    break
            except:
                break

        ticker = ticker.upper()
        if len(ticker) > 6:
            continue
        # if ticker != "":
        #   print(ticker)

        if ticker not in all_stocks:
            all_stocks.append(ticker)
            rankings[ticker] = 1

        elif ticker in all_stocks:
            rankings[ticker] += 1
        # print(all_stocks)

        largest = nlargest(5, rankings, key=rankings.get)

        for i in range(len(largest) - 1):
            a = largest[i]
            no_dollar = a[1:]
            try:
                stock_prices[largest[i]] = get_price(no_dollar)
            except:
                continue
        # print(rankings)
        for i in range(len(largest)-1):
            amount[largest[i]] = rankings[largest[i]]
        print(amount)
        print(largest)
        print(stock_prices)
