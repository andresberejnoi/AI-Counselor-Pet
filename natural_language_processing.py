'''NLP-related code will go here'''
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import text2emotion as te


import paralleldots

import pandas as pd
import os

from settings import PARALLELBOTS_API_KEY

def guess_emotion(text, analyzer):
    '''Analyzer is the sentiment analyzer from nltk, at least for now'''
    result = analyzer.polarity_scores(text)
    return result


class Text2EmotionAnalyzer(object):
    "this should not be a class"
    def guess_emotion(self, text):
        result = te.get_emotion(text)
        return result


class NLTKEmotionAnalyzer(object):
    "I should probably turn this into a function"
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def guess_sentiment(self, text):
        result = self.analyzer.polarity_scores(text)  #this is a dictionary
        highest = 0
        emotion_highest = ''
        for emotion in result:
            val = result[emotion]
            if val > highest:
                highest = val
                emotion_highest = emotion 
        return emotion_highest, highest    #emotion and its likelihood value
    
class ParallelDotsEmotionAnalyzer(object):
    "This should also be simply a function and not a full class"
    def __init__(self):
        paralleldots.set_api_key(PARALLELBOTS_API_KEY)

    def guess_emotion(self, text):
        result = paralleldots.sentiment(text)
        return result