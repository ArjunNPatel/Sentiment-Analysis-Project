import csv
#pip install nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize
#nltk.download("punkt")
#nltk.dowload('vader_lexicon')
#We would like to thank NLTK (Natural Language Toolkit)
#Bird, Steven, Edward Loper and Ewan Klein (2009), Natural Language Processing with Python. O’Reilly Media Inc.


# GLOBALS
total = 0.0
values = {
    "pos": 0.0,
    "neg": 0.0,
    "neu": 0.0,
    "compound": 0.0
}
sentiment = SentimentIntensityAnalyzer()
#values = [neg, neu, pos, compound]
def analyze_sentiment(file_name, ticker):
    global total, values
    with open("ec_results" + ticker + ".csv", mode = "w") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Date of Call", "Negative", "Neutral", "Positive", "Compound"])
    with open(file_name, mode = "r") as readfile:
        csv_reader = csv.DictReader(readfile,delimiter= ",", skipinitialspace = True)

        for row in csv_reader:
            sentences = sent_tokenize(row["Text"])
            with open("ec_results" + ticker + ".csv", mode = "a") as f:
                writer = csv.writer(f)
                try:
                    values["pos"]= 0.0
                    values["neg"] = 0.0
                    values["neu"] = 0.0
                    values["compound"] = 0.0
                    total = 0.0
                    for sentence in sentences:
                        sentiment_calulation(sentence)
                    print(total)
                    print(row.keys())
                    writer.writerow([ 
                        row["Name"], 
                        row["Date"],  
                        values["neg"]/total,
                        values["neu"]/total,
                        values["pos"]/total,
                        values["compound"]/total  
                        ])
                    
                except ZeroDivisionError:
                    print("There was no data to analyze.\n")
                except Exception as e:
                    print(e)

def sentiment_calulation(text):
    global total, values
    weight = 1
    sentence_values = sentiment.polarity_scores(text)
    values["pos"] += weight*sentence_values["pos"]
    values["neg"] += weight*sentence_values["neg"]
    values["neu"] += weight*sentence_values["neu"]
    values["compound"] += weight*sentence_values["compound"]
    total += weight
    

if __name__ == '__main__':
    analyze_sentiment("/home/arjunnipatel/earnings_calls_MSFT.csv", "MSFT")
