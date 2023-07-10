#this code will get sections 1 and 7A from the lastest 10k SEC filings for various companies. It tries to collect up to a decade of data.
import csv
from sec_api import QueryApi
import csv
from sec_api import ExtractorApi
from bs4 import BeautifulSoup



KEY = "YOUR KEY"
myExtractor = ExtractorApi(KEY)
myQuery = QueryApi(api_key = KEY)
def collect(ticker_list):
    ten_k_list = []
    for ticker in ticker_list:
        ten_k_list.append(recent_Ten_k(ticker))
    
    for x in range(0,len(ticker_list)):
        extract_section_text(ticker_list[x],ten_k_list[x])


def recent_Ten_k(ticker):
    query = {
    "query": {
        "query_string": {
            "query": "ticker: " + ticker  +  " AND formType:\"10-K\""
           
        }
    },
    "from": "0",
    "size": "10",
    "sort": [{ "filedAt": { "order": "desc" } }]
    }
    queryResponse = myQuery.get_filings(query)
    filings = queryResponse["filings"]
    #we cannot handle non html files
    for filing in filings:
        if filing["linkToFilingDetails"][-3:] != "htm" and  filing["linkToFilingDetails"][-4:] != "html":
            filing["linkToFilingDetails"] = "No Link"
        
    return filings


def extract_section_text(ticker, filings):    
    with open( "sec_data" + str(ticker) + ".csv", mode='w', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Name", "Date of 10k Filing", "1A", "7"])
        for filing in filings:
            filing_url = filing["linkToFilingDetails"]
            section_text = myExtractor.get_section(filing_url, "1A", "text")
            section_html = myExtractor.get_section(filing_url, "7", "html")
            soup = BeautifulSoup(section_html, 'html.parser')
            section_text_html_stripped = soup.get_text()
            writer.writerow([ticker, filing["filedAt"], section_text, section_text_html_stripped])


if __name__ == "__main__":
    collect(["AAPL"])
