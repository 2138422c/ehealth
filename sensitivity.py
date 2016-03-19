__author__ = 'alistaircross'

"""
    This program requires both textblob and textstat plugins for python
    It will return the sensitivity rating of a text object
    This sensitivity will be a dictionary:
        overall sensitvity
        sentiment
        readability
"""
from textblob import TextBlob
from textstat.textstat import textstat

def  get_sensitivity_rating(text):
    blob = TextBlob(text)
    d = { "sentimentality":blob.subjectivity * 100,
        "readability":textstat.flesch_reading_ease(text)}
    # subjectivity is a float between 0 and 1, multiplied it by 100 so it's percent
    # The overall sensitivity of teh article is the readability minus the subjectivity
    d["sensitivity"] = (d["readability"] - d["sentimentality"])
    return d
