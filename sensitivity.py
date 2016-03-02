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
    sentimentality = blob.subjectivity * 100
    readability = textstat.flesch_reading_ease(text)
    sensitivity = (sentimentality + readability)/2
    print "Sensitivity:", sensitivity
    if sensitivity < 50:
        print "This article may not handle the subject in a sensitive manner. \n\n"
    print "Subjectivity:", sentimentality
    if sentimentality < 50:
        print "This article may loaded with subjectivity.\n\n"
    print "Readability:", readability
    if readability < 50:
        print "This article contains content that is difficult to understand\n\n"

get_sensitivity_rating(text) # Remove this when we're ready to implement
