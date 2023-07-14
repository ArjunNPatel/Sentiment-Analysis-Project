"""
EDGAR API is quite difficult to use, but if someone could figure out how to extract 10-K section 1a and 7 using it, 
this project could scale up more easily and money would be saved in not buying the SEC-API.IO service.
The Scraper is started here.
"""
import csv
import requests
from bs4 import BeautifulSoup
import json
import re
#GLOBALS
agent_header = {
        "User-Agent": "UCONN Arjun",
        "Accept-Encoding": "gzip, deflate",
        "Host": "data.sec.gov"
    }
def collect(ticker_list):
    ten_k_list = []
    for ticker in ticker_list:
        ten_k_list.append(recent_Ten_k(ticker))
    for x in range(0, len(ticker_list)):
        extract_section_text(ticker_list[x], ten_k_list[x])
    print("Yay!")

def recent_Ten_k(ticker):
    global agent_header
    while(len(ticker) < 10):
        ticker = "0" + ticker
    query_url = f"https://data.sec.gov/submissions/CIK{ticker}.json"
    #print(query_url)
    #print(query_url == "https://data.sec.gov/submissions/CIK0000829224.json")
    
    response = requests.get(query_url, headers = agent_header )
    info = json.loads(response.text)
    filings = []
    for i in range(len(info["filings"]["recent"]["filingDate"])):
        if info["filings"]["recent"]["form"][i] == "10-K":
            filings.append({
            "linkToFilingDetails": info["filings"]["recent"]["accessionNumber"][i],
            "filedAt": info["filings"]["recent"]["acceptanceDateTime"][i][0:-5]
            })
    
    return filings

def extract_section_text(ticker, filings):    
    global agent_header
    with open(f"sec_data{ticker}.csv", mode='w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Name", "Date of 10k Filing", "1A", "7"])
        
        for filing in filings:
          #  print(filing)
            """https://www.sec.gov/Archives/edgar/data/1122304/000119312515118890/0001193125-15-118890.txt"""
            no_dashes_accession = re.sub('[^0-9]','', filing["linkToFilingDetails"])
            #print(no_dashes_accession)
            filing_url = f"https://www.sec.gov/Archives/edgar/data/{ticker}/{no_dashes_accession}/{filing['linkToFilingDetails']}.txt"
          #  print(filing_url)
            response = requests.get(filing_url, headers = {
                "User-Agent": "UCONN Arjun",
                "Accept-Encoding": "gzip, deflate",
                "Host": "www.sec.gov"
            })
           # print(response)
            soup = BeautifulSoup(response.text, 'html.parser')
            writer.writerow([ticker, filing["filedAt"], re.sub("<.*?>", "", soup.get_text())[0:8000],""])
            

if __name__ == "__main__":
    #must use CIK numbers
    collect(["50863"])
