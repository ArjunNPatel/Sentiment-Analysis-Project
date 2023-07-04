#this code will get sections 1 and 7A from the lastest 10k SEC filings for various companies.
import csv
#pip install with this if sec is giving error (without the quotes): 'pip install sec-api'
from sec_api import QueryApi
import csv
from sec_api import ExtractorApi
from bs4 import BeautifulSoup




myExtractor = ExtractorApi("KEY HERE")
myQuery = QueryApi(api_key = "KEY HERE")
def main():
    ticker_list = ["AAPL" , "IBM", "SBUX"]
    ten_k_list = []
    for ticker in ticker_list:
        ten_k_list.append(recent_Ten_k(ticker))




    #ticker_list and ten_k_html_list should be same length
    for x in range(0,len(ticker_list)):
        # Thanks to Code from Haris; HarisMahmood8
        if(ten_k_list[x] != "No Link"):
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
    print(filing_url)
    section_text = myExtractor.get_section(filing_url, "1A", "text")
    section_html = myExtractor.get_section(filing_url, "7", "html")
    soup = BeautifulSoup(section_html, 'html.parser')
    section_text_html_stripped = soup.get_text()
    with open( "sec_data" + str(ticker) + ".csv", mode='w', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Section', 'Content'])
        writer.writerow(['Name', str(ticker)])
        writer.writerow(['Date of 10k Filing', ten_k["filedAt"]])
        writer.writerow(['1A', section_text])
        writer.writerow(['7', section_text_html_stripped])


if __name__ == "__main__":
    main()
