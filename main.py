import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape(num):
    # clean num input from user
    num = int(num)
    num = min(num,50)
    num = max(0,num)
    try:
        # get API data from API
        wsb = requests.get("https://tradestie.com/api/v1/apps/reddit")
        wsb = wsb.json()
        tickers = dict()
        added = []
        while True:
            # ask users for stocks to add to portfolio
            addtickers = input("Please input ticker symbols you would like to add. Enter NONE to stop:")
            if addtickers.strip().lower() == "none":
                break
            if addtickers == '':
                continue
            added.append({"no_of_comments": 0, "sentiment": "N/A", "sentiment_score": 0.0, "ticker": addtickers.upper()})  
        for stock in wsb[:num]+added:
            if stock['ticker'] in list(tickers.keys()):
                continue
            tickers[stock["ticker"]] = {"no_of_comments": stock["no_of_comments"], "sentiment": stock["sentiment"], "sentiment_score": stock["sentiment_score"]}
            # scrape yahoo finance page of stock
            response = requests.get(f"https://finance.yahoo.com/quote/{stock["ticker"]}/")
            if response.status_code != 200:
                print(f"{stock} couldn't be found")
                continue
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find("div", attrs={"data-testid": "quote-statistics"})
            data = table.text.split("  ")
            data = [l.strip() for l in data]
            columns = []
            # interpret and clean scraped data from yahoo finance. Pass data into a dictionary
            for cell in data:
                n = cell.split(' ')
                col = ''
                if 'Date' in n:
                    col = ' '.join(n[:2])
                    tickers[stock["ticker"]][col] = ''.join(n[2:])
                elif 'x' in n or '-' in n:
                    col = ' '.join(n[:-3])
                    tickers[stock["ticker"]][col] = ''.join(n[-3:])
                elif '%' in n:
                    col =  ' '.join(n[:-2])
                    tickers[stock["ticker"]][col] = ''.join(n[-2:])
                else:
                    col = ' '.join(n[:-1])
                    tickers[stock["ticker"]][col] = ''.join(n[-1])
                if col not in columns:
                    columns.append(col)
        c = ['Ticker', "no_of_comments", "sentiment", "sentiment_score"] + columns + ["Earnings Date", "Ex-Dividend Date"]
        # create cleaned dictionary to pass into DataFrame
        fin = dict()
        for i in range(len(c)):
            fin[c[i]] = []
            for j in range(len(tickers.keys())):
                if i==0:
                    fin[c[i]].append(list(tickers.keys())[j])
                else:
                    if c[i] in tickers[list(tickers.keys())[j]].keys():
                        fin[c[i]].append(tickers[list(tickers.keys())[j]][c[i]])
                    else:
                        fin[c[i]].append("--")
        df = pd.DataFrame(fin)
        return df
        
    except Exception as e:
        print(f"An error has occured: {e}")

def main():
    #ask user how many stocks from Wall Street Bets they want to see
    print("View Top [1 to 50] Stocks on Wall Street Bets")
    # error handle user input
    number = 'x'
    while not number.isnumeric():
        number = input("Enter a number from 1 through 50: ")
    # call scrape(num) function and convert outputted DataFrame into a CSV
    df = scrape(number)
    df.to_csv("top5_on_wsb.csv",index=False)

if __name__ == "__main__":
    main()