"""
The code used to get the 10k data struggles with HTML entities that are used to represent special characters
https://www.freeformatter.com/html-entities.html
https://www.w3schools.com/html/html_entities.asp  

This code will revert those characters back from their entity number to the actual format.

In other words, this cleans the text so it because human-readable.
"""
import re
import csv
def main():
    file_name = "sec_dataIBM copy.csv" 
    section_name = []
    section_text = []
    with open(file_name) as readfile:
        csv_reader = csv.reader(readfile,delimiter= ",")
        for row in csv_reader:
            section_name.append(row[0])
            section_text.append(row[1])

    for i in range(len(section_text)):
        section_text[i] = clean(section_text[i])

    with open(file_name, mode = "w") as writefile:
        writer = csv.writer(writefile)
        for i in range(len(section_text)):
            writer.writerow([section_name[i], section_text[i]])
    print("Success!")
def clean(text):
    replace = {
        #symbols that are not needed
        "&#8226;": "",
        "&#8203;": "",
        #dashes
        "&#8212;":"—",
        "&#8209;": "-",
        "&#8211;": "-",
        #quotations and ampersands
        "&#8220;": "\"",
        "&#8221;": "\"",
        "&#8217;":"\'",
        "&#38": "&"        
    }
    #getting back apostrophes
    for key in replace:
        text = re.sub(key, replace[key], text)
    return text



if __name__ == "__main__":
    main()
