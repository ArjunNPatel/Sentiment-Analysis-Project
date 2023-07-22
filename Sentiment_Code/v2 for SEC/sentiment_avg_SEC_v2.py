#this is version_2 possibly
import csv
#pip install nltk
from nltk.sentiment.vader import *
from nltk.tokenize import sent_tokenize
from classifierv2SEC import *
#nltk.download("punkt")
#nltk.dowload('vader_lexicon')
#We would like to thank NLTK (Natural Language Toolkit)
#Bird, Steven, Edward Loper and Ewan Klein (2009), Natural Language Processing with Python. O’Reilly Media Inc.
def custom_finance_VADER(vader_model):
    lexicon_add = {
    "sale":2,
    "sales":2,
    "retail":1,
    "store":1,
    "stores":1,
    "revenue":4,
    "demand":3,
    "lawsuit":-4,
    "litigation":-3,
    "expense":-1,
    "expenses":-1,
    "cost":-2,
    "costs":-2,
    "competition":-1,
    "profit":4,
    "profits":4,
    "income":4,
    "decrease":-4,
    "decreased":-4
    }
    good_boosters = "believe project expect anticipate estimate intend strategy future opportunity plan should will would increase increased grow grew growth"
    bad_boosters = "may might could potentially"
    negate_tokens = "decrease decreased decline declined"
    for token in good_boosters.split(" "):
        VaderConstants.BOOSTER_DICT[token] =  VaderConstants.B_INCR
    for token in bad_boosters.split(" "):
        VaderConstants.BOOSTER_DICT[token] =  VaderConstants.B_DECR
    for token in negate_tokens.split(" "):
        VaderConstants.NEGATE.add(token)
    VaderConstants.SPECIAL_CASE_IDIOMS["cost of revenue"] = -2
    vader_model.lexicon.update(lexicon_add)


# GLOBALS
total = 0.0
values = {
    "pos": 0.0,
    "neg": 0.0,
    "neu": 0.0,
    "compound": 0.0
}
sentiment = SentimentIntensityAnalyzer()
custom_finance_VADER(sentiment)
#values = [neg, neu, pos, compound]
def analyze_sentiment(file_name, ticker):
    global total, values
    with open("results" + ticker + " (v2).csv", mode = "w") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Date of 10k Filing", "Negative", "Neutral", "Positive", "Compound"])
    with open(file_name, mode = "r") as readfile:
        csv_reader = csv.DictReader(readfile,delimiter= ",")

        for row in csv_reader:
            Section_1A = sent_tokenize(row["1A"])
            Section_7 = sent_tokenize(row["7"])
            sentences = Section_1A + Section_7
            weight_list = test_sentences(sentences)
            with open("results" + ticker + " (v2).csv", mode = "a") as f:
                writer = csv.writer(f)
                try:
                    values["pos"]= 0.0
                    values["neg"] = 0.0
                    values["neu"] = 0.0
                    values["compound"] = 0.0
                    total = 0.0 
                    for i in range(len(sentences)):
                        if weight_list[i] == 0:
                            continue
                        sentiment_calulation(sentences[i])
                    #sentiment_calulation(row["1A"] + row["7"])
                    writer.writerow([ 
                        row["Name"], 
                        row["Date of 10k Filing"],  
                        values["neg"]/total,
                        values["neu"]/total,
                        values["pos"]/total,
                        values["compound"]/total, 
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

    #print(values["pos"])



if __name__ == '__main__':
    analyze_sentiment("/home/arjunnipatel/sec_dataMSFT.csv", "MSFT")
