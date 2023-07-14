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
# taking input as the date
def stock_history_correlation(file_name, ticker, forward):
    def bad_date(Date):
        if forward == "2yr" and Begindate + timedelta(days = int(2*365)) > datetime.now():
            return True
        elif forward == "18mo" and Begindate + timedelta(days = int(3*365/2)) > datetime.now():
            return True
        elif forward == "1yr" and Begindate + timedelta(days = int(365)) > datetime.now():
            return True
        elif forward == "6mo" and Begindate + timedelta(days = int(365/2)) > datetime.now():
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
            Begindate = datetime.strptime(row["Date of 10k Filing"][0:10], "%Y-%m-%d")
            if(bad_date(Begindate)):
                continue
            future_from_date.append( {
                    "Date":Begindate,
                    "Date Stock":adj_close(Begindate, history),
                    "Date + 6mo Stock": adj_close(Begindate + timedelta(days= int(365/2)), history),
                    "Date + 1yr Stock": adj_close(Begindate + timedelta(days= int(365)), history),
                    "Date + 18mo Stock": adj_close(Begindate + timedelta(days= int(3*365/2)), history),
                    "Date + 2yr Stock": adj_close(Begindate + timedelta(days= int(2*365)), history),
            })
            x.append(float(row["Compound"]))


    x = np.array(x)
    y = []
    #change here to either 6mo, 1yr, 18mo, or 2yr
    for date in future_from_date:
        
        y.append( (date[f"Date + {forward} Stock"] -  date["Date Stock"]) / date["Date Stock"]  )
    y = np.array(y)
    print(x)
    print(y)
    plt.plot(x,y,'o')
    plt.xlabel("Compound Sentiment Score of the 10k")
    #plt.xticks(ticks = x, labels = list(map(lambda v: str(v)[0:4], x)), rotation = 45)
    plt.ylabel(f"Percent Growth of the Stock over {forward} after filing the 10k")
    

    plt.savefig(ticker + f" {forward} vs Compound Sentiment.png", bbox_inches = "tight")
    


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
    stock_history_correlation("/home/arjunnipatel/resultsMSFT.csv", "MSFT", "1yr")
