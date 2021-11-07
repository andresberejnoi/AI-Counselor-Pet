'''NLP-related code will go here'''
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

import pandas as pd
import os

def guess_emotion(text, analyzer):
    '''Analyzer is the sentiment analyzer from nltk, at least for now'''
    result = analyzer.polarity_scores(text)
    return result

                
class NLTKEmotionAnalyzer(object):
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def guess_emotion(self, text):
        result = self.analyzer.polarity_scores(text)  #this is a dictionary
        highest = 0
        emotion_highest = ''
        for emotion in result:
            val = result[emotion]
            if val > highest:
                highest = val
                emotion_highest = emotion 
        return emotion_highest, highest    #emotion and its likelihood value
    
