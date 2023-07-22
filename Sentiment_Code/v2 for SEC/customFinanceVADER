from nltk.sentiment.vader import *

thing = SentimentIntensityAnalyzer()
company = open("COMPANYv2SEC.txt", mode = 'r')
lst = [ s.strip() for s in company]
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
    "income":4
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
thing.lexicon.update(lexicon_add)
for text in lst:
    vals = thing.polarity_scores(text)
    if vals["neg"] > .1:
        print(text)
        print(vals)
        print("*"*100)
