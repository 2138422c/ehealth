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

text = "The quick brown fox jumped over the lazy dog." # Replace with actual text when available

def  get_sensitivity_rating(text):
    blob = TextBlob(text)
    sentimentality = blob.subjectivity * 100 # Turned scores into percentages to make it easier for user to understand
    readability = textstat.flesch_reading_ease(text)
    sensitivity = (sentimentality + readability)/2 # Overall average sensitivity

get_sensitivity_rating(text) # Remove this when we're ready to implement
