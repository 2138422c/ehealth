__author__ = 'alistaircross'

"""
    This program requires both textblob and textstat plugins for python
    It will return the sensitivity rating of a text object
    This sensitivity will be a dictionary:
        overall sensitvity
        sentiment
        length
        readability
"""
from textblob import TextBlob
from textstat.textstat import textstat

text = "The quick brown fox jumped over the lazy dog." # Replace with actual text when available

blob = TextBlob(text)
sentimentality = blob.subjectivity * 100
readability = textstat.automated_readability_index(text) * 10