"""
Produces a scatterplot of the sentiment score from the 10k versus the stock percent change ((new - original) / original) in value. 
Original is the adj close stock value on a day closest to the filing of the 10k.
New is the adj close stock value on a day closest to {6months, 1 year, 18months, 2 years} after the filing of the 10k.
Soon we will add regression to this.
"""
import yfinance as yf
from datetime import datetime
from datetime import timedelta
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from regression_analysis import LinearModel
# taking input as the date
def stock_history_correlation(
    file_name, 
    ticker, 
    forward, 
    corpus_type,
    xlabel = "S_wa", 
    ylabel = "R_st",
    ):
    def bad_date(Date):
        if forward == "2yr" and Begindate + timedelta(days = int(2*365)) > datetime.now():
            return True
        elif forward == "18mo" and Begindate + timedelta(days = int(3*365/2)) > datetime.now():
            return True
        elif forward == "1yr" and Begindate + timedelta(days = int(365)) > datetime.now():
            return True
        elif forward == "6mo" and Begindate + timedelta(days = int(365/2)) > datetime.now():
            return True
        elif forward == "3mo" and Begindate + timedelta(days = int(365/4)) > datetime.now():
            return True
        return False
    history = yf.download(ticker, interval="1d")
    history["date"] = history.index
    future_from_date = []
    x = []
    #current, 6mo,12mo,18mo,24mo
    with open(file_name) as readfile:
        csv_reader = csv.DictReader(readfile,delimiter= ",")
        for row in csv_reader:
            date_header = "Date of 10k Filing"
            if corpus_type == "Earnings Call":
                date_header = "Date of Earnings Call"
            Begindate = datetime.strptime(row[date_header][0:10], "%Y-%m-%d")
            if(bad_date(Begindate)):
                continue
            future_from_date.append( {
                    "Date":Begindate,
                    "Date Stock":adj_close(Begindate, history),
                    "Date + 3mo Stock": adj_close(Begindate + timedelta(days = int(365/4)), history),
                    "Date + 6mo Stock": adj_close(Begindate + timedelta(days= int(365/2)), history),
                    "Date + 1yr Stock": adj_close(Begindate + timedelta(days= int(365)), history),
                    "Date + 18mo Stock": adj_close(Begindate + timedelta(days= int(3*365/2)), history),
                    "Date + 2yr Stock": adj_close(Begindate + timedelta(days= int(2*365)), history),
            })
            x.append(float(row["Compound"]))


    x = np.array(x)
    y = []
    for date in future_from_date:
        y.append( (date[f"Date + {forward} Stock"] -  date["Date Stock"]) / date["Date Stock"]  )
    y = np.array(y)
    print(x)
    print(y)


    plt.plot(x,y,'o')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    info = LinearModel(x,y)
    """" info = {
        "Text": Text,
        "R2": model.score(x,y),
        "Coef": model.coef_,
        "Intercept": model.intercept_
    }"""
    line_input = np.linspace(min(x), max(x))
    plt.plot(line_input, info["Coef"][0]*line_input + info["Intercept"], label = info["Text"], c = 'red' )
    plt.legend(loc='best')
    plt.title(f' Compound Sentiment Score on {ticker}_{corpus_type} vs {forward} Return')
    plt.savefig(f"{ticker}_{corpus_type}_{forward} Compound Sentiment.png")
    


def adj_close(date, history):
    lo = 0
    hi = len(history)-1
    while(hi != lo):
        mid = int((lo + hi)/2)
        midDate = datetime.strptime(str(history.iloc[mid]["date"])[0:10], "%Y-%m-%d") 
        if midDate > date:
            hi = mid
        else:
            lo = mid+1
    return history.iloc[lo]["Adj Close"] 
if __name__ == "__main__":
    stock_history_correlation("resultsAAPL.csv", "AAPL", "1yr","10K")
