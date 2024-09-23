import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape(num):
    num = min(num,50)
    num = max(0,num)
    try:
        wsb = requests.get("https://tradestie.com/api/v1/apps/reddit")
        wsb = wsb.json()
        tickers = dict()
        added = []
        while True:
            addtickers = input("Please input ticker symbols you would like to add. Enter NONE to stop:")
            if addtickers.strip().lower() == "none":
                break
            added.append({"no_of_comments": 0, "sentiment": "N/A", "sentiment_score": 0.0, "ticker": addtickers.upper()})  
        for stock in wsb[:num]+added:
            tickers[stock["ticker"]] = {"no_of_comments": stock["no_of_comments"], "sentiment": stock["sentiment"], "sentiment_score": stock["sentiment_score"]}
            response = requests.get(f"https://finance.yahoo.com/quote/{stock["ticker"]}/")
            if response.status_code != 200:
                print(f"{stock} couldn't be found")
                continue
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find("div", attrs={"data-testid": "quote-statistics"})
            data = table.text.split("  ")
            data = [l.strip() for l in data]
            columns = []
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
        print(tickers)
        return df
        
    except Exception as e:
        print(f"An error has occured: {e}")

def main():
    df = scrape(5)
    df.to_csv("top5_on_wsb.csv",index=False)

if __name__ == "__main__":
    main()