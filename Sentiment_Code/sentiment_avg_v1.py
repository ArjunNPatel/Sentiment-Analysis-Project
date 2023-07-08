"""
Splits the text from section 1A and 7 of a 10k filing CSV into setencnes. Analyzes each sentence with sentiment analysis. 
Takes the average of the scores and magnitudes.
One drawback of this is the values generated from each sentences contributes equally to each sentence. 
(In the weighted average calculation, all sentences recieve the weight of 1). 
For example:
A company writes "Frustration with customer support remains a *very minor* cause of social tensions".
The next sentence is "*Very minor* growth in earnings expected from new product".
The second sentence should be weighted higher because earnings tracks stock value very closely, while social tensions does not necessarily do so.
"""

import csv
# Imports the Google Cloud client library
from google.cloud import language_v1
from google.cloud import language
#pip install nltk
from nltk import *
#nltk.download("punkt")
#We would like to thank NLTK (Natural Language Toolkit)
#Bird, Steven, Edward Loper and Ewan Klein (2009), Natural Language Processing with Python. O’Reilly Media Inc.


# GLOBALS
client = language.LanguageServiceClient.from_service_account_json("/home/arjunnipatel/2023summer/auth.json")
total = 0.0
score = 0.0
mag = 0.0
def main():
    sentences = []
    file_name = "/home/arjunnipatel/2023summer/sectest.csv"
    with open(file_name, mode = "r") as readfile:
        csv_reader = csv.reader(readfile,delimiter= ",")
        rows = list(csv_reader)
        string1A = rows[3][1]
        Section_1A = sent_tokenize(string1A)
        string7 = rows[4][1]
        Section_7 = sent_tokenize(string7)
        sentences = Section_1A + Section_7
    with open("results.txt", mode = "w") as f:
        try:
            for sentence in sentences:
                print(sentence)
                f.write(sentence + "\n")
                temp_values = figure(sentence)
                f.write(str(temp_values[0]) + " " + str(temp_values[1]) + "\n")
            f.write("The weighted average score of the text is " + str(score / total) + "\n")
            f.write("The weighted average magnitude of the text is " + str(mag / total) + "\n")
        except ZeroDivisionError:
            f.write("There was no data to analyze.\n")
        except Exception as e:
            f.write("Something else went wrong.\n")
            f.write(e)
            print(e)

def figure(text):
    global total, score, mag
    document = language_v1.types.Document(
        content=text, type_=language_v1.types.Document.Type.PLAIN_TEXT
    )

    # Detects the sentiment of the text
    response = client.analyze_sentiment(
        request={"document": document}
    ).document_sentiment
    weight = 1
    t_score =  response.score
    t_mag = response.magnitude
    total +=  weight
    score += t_score*weight
    mag += t_mag*weight
    print(t_score)
    print(t_mag)
    return [t_score, t_mag]

if __name__ == '__main__':
    main()
