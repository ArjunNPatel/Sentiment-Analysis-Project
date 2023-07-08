# Sentiment-Analysis-Project
This project is part of research work at the University of Connecticut-Stamford Campus. 
### Definitions
A company is any business whose stock is listed on a U.S. stock exchange or whose securities are publicly offered in the United States.


Business outlook is a qualitative measure of how a company believes it will perform financially, especially in the short-term. For example, if a company believes its new product will have a record number of sales, that is a positive business outlook. As another example, if a company thinks that it will experience supply-chain issues, thus taking loss in the near future, that is a negative business outlook. The term outlook is also used. The goal is to quantify this and see how it causes changes in stock value.


### Define the Problem
Predict the future stock prices of a variety of companies. Develop a model of the stock market that uses high-quality sources; the model should be accurate.
### Assumptions
1. If a company is generally positive and/or optimistic about its business (positive outlook), the price of the stock will increase. If a company is generally negative and/or pessimistic about its business (negative outlook), the price of the stock will decrease.
*Justification: a company that thinks it will do well in the future acts more confident in front of investors. As a result, investors will drive the price of the stock up. A company that does not think it will do well will act less confident, making investors nervous or skeptical. This could drive the stock price down.*  
2. All companies will describe their outlook truthfully in a legal filing with the SEC, such as a 10-k report.
 *Justification: a company that lies about their financial or economic situation in a report to the SEC might face severe legal consequences. Most companies would not take that risk. So, they would provide the truth about their business outlook.*  
3. All companies will describe their outlook truthfully in an earnings call.
*Justification: if a company lies to their investors or romanticizes their situation, and then does not perform as expected, investors would lose trust in the company. This could cause social and economic consequences for the company and would possibly incur a loss greater than simply admitting to the true expected earnings. Most companies would take the lesser risk and answer questions on earnings calls with the truth.*

### Variables and Data

### The Model
Sentiment analysis is any algorithm that takes in a piece of text and returns some quantitative data on the emotional value of that text. SEC legal filings and earnings call transcripts will provide a significant amount of text to analyze. If the sentiment analysis algorithms deems that the majority of the text has positive emotional value, the company clearly has a positive outlook. Thus, we can infer the stock price will increase. By the same logic, if the text collected has negative emotional value according to the sentiment analysis algorithm, the company has a negative outlook (the stock price will decrease).

