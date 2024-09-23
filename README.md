# Wall Street Bets Stock Portfolio
I'm using an API to gather the top 50 most talked about stocks on Reddit forum r/wallstreetbets and storing their number of comments, sentiment, and sentiment score. I'm scraping stock data from Yahoo Finance. I chose this website because it contains valuable, up-to-date stock information.

## Value from Dataset
This dataset allows users to see and compare stock information from Yahoo Finance and r/wallstreetbets. This is useful when analyzing stocks because you can see daily information on a stock next to the overall sentiment of the stock on r/wallstreetbets. 
This dataset isn't publicly available because sentiment and daily stock data is constantly changing.

## Instructions to Run
1. Run this command in the terminal
```https://github.com/ianjiang7/WSB_Stock_Portfolio.git```
2. cd in the directory and set up a virtual environment
```python -m venv .venv```
3. Activate venv in Windows:
```.venv\Scripts\activate```
Activate on macOS and Linux:
```source .venv/bin/activate```
4. Install requirements
```pip install -r requirements.txt```
5. Run the main function
```python3 main.py```