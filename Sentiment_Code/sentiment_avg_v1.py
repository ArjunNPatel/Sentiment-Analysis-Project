# Imports the Google Cloud client library
from google.cloud import language_v1
from google.cloud import language


# GLOBALS
client = language_v1.LanguageServiceClient()


def main():
    # The text to analyze
    #these are real quotes from SBUX 10k report for 2022
    text = {
    "We believe we have built an excellent reputation globally for the quality of our products, for delivery of a consistently positive consumer experience and for our global social and environmental impact programs",
    "During fiscal 2021 and continuing into fiscal 2022, we experienced certain supply shortages and transportation delays largely attributable to impacts of the COVID-19 pandemic as well as changes in customer demand and behaviors",
    "While we expect these shortages and delays may continue into fiscal 2023, we view them to be temporary and do not believe they will have a material impact to our long-term growth and profitability"
    }
    for sentence in text:
        sentiment(sentence)


def sentiment(sentence):
    document = language_v1.types.Document(
        content=sentence, type_=language_v1.types.Document.Type.PLAIN_TEXT
    )


    # Detects the sentiment of the text
    response = client.analyze_sentiment(
        request={"document": document}
    ).document_sentiment
    print(sentence)
    print(str(response.score) + " " + str(response.magnitude))
   
if __name__ == "__main__":
    main()


