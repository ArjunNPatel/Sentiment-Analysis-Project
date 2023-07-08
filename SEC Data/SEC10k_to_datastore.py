from sec_api import QueryApi
import csv
from sec_api import ExtractorApi
from bs4 import BeautifulSoup
from google.cloud import datastore
#GLOBALS
myExtractor = ExtractorApi("YOUR KEY HERE")
myQuery = QueryApi(api_key = "YOUR KEY HERE")
datastore_client = datastore.Client()
def main():
    ticker_list = ["SBUX","AAPL"]
    ten_k_list = []
    for ticker in ticker_list:
        ten_k_list.append(recent_Ten_k(ticker))




    #ticker_list and ten_k_html_list should be same length
    for x in range(0,len(ticker_list)):
        # Thanks to Code from Haris; HarisMahmood8
        if(ten_k_list[x] != "No Link"):
            print("Now extracting " + ticker_list[x] + " data")
            extract_section_text(ticker_list[x],ten_k_list[x])


def recent_Ten_k(ticker):
    query = {
    "query": {
        "query_string": {
            "query": "ticker: " + ticker  +  " AND formType:\"10-K\""
           
        }
    },
    "from": "0",
    "size": "1",
    "sort": [{ "filedAt": { "order": "desc" } }]
    }
    queryResponse = myQuery.get_filings(query)
    filings = queryResponse["filings"][0]
    #we cannot handle non html files
    if filings["linkToFilingDetails"][-3:] != "htm" and  filings["linkToFilingDetails"][-4:] != "html":
        filings["linkToFilingDetails"] = "No Link"
    return filings


def extract_section_text(ticker, ten_k):
    filing_url = ten_k["linkToFilingDetails"]
    #print(filing_url)
    section_text = myExtractor.get_section(filing_url, "1A", "text")
    section_html = myExtractor.get_section(filing_url, "7", "html")
    soup = BeautifulSoup(section_html, 'html.parser')
    section_text_html_stripped = soup.get_text()
    # The kind for the new entity
    kind = '10k_company_data'
    # The name/ID for the new entity
    name = ticker + " data" + ten_k["filedAt"][0:4]
    # The Cloud Datastore key for the new entity
    task_key = datastore_client.key(kind, name)
    # Prepares the new entity
    task = datastore.Entity(key=task_key,exclude_from_indexes= ['Section 1A', 'Section 7'])
    task['Date of 10k Filing'] = ten_k["filedAt"]
    task['Section 1A'] = section_text
    task['Section 7'] = section_text_html_stripped
    task['Ticker/Company'] = ticker
    # Saves the entity
    print("data saving now...")
    datastore_client.put(task)
   


if __name__ == "__main__":
    main()




