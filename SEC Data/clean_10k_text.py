"""
The code used to get the 10k data struggles with HTML entities that are used to represent special characters
https://www.freeformatter.com/html-entities.html
https://www.w3schools.com/html/html_entities.asp  

This code will revert those characters back from their entity number to the actual format.

In other words, this cleans the text so it because human-readable.
"""
import re
import csv
def clean_csv(file_name): 
    csv_rows = []
    with open(file_name) as readfile:
        csv_reader = csv.DictReader(readfile,delimiter= ",")
        for row in csv_reader:
            csv_rows.append([row["Name"], row["Date of 10k Filing"], clean(row["1A"]), clean(row["7"])])
            

    with open(file_name, mode = "w") as writefile:
        writer = csv.writer(writefile)
        writer.writerow(["Name", "Date of 10k Filing", "1A", "7"])
        for row in csv_rows:
            writer.writerow([row[0], row[1], row[2], row[3]])
    print("Success!")
def clean(text):
    replace = {
        #symbols that are not needed
        "&#8226;": "",
        "&#8203;": "",
        "&#160;": "",
        #dashes
        "&#8212;":"—",
        "&#8209;": "-",
        "&#8211;": "-",
        #quotations and ampersands
        "&#8220;": "\"",
        "&#8221;": "\"",
        "&#8217;":"\'",
        "&#146;": "\'",
        "&#147;": "\"",
        "&#148;": "\"",
        "&#38;": "&"        
    }
    #getting back apostrophes
    for key in replace:
        text = re.sub(key, replace[key], text)
    text = re.sub("&#.*?;", "", text)
    return text



if __name__ == "__main__":
    clean_csv("sec_dataAAPL.csv")
