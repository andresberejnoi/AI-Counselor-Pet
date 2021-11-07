#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      pzin
#
# Created:     07/11/2021
# Copyright:   (c) pzin 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from natural_language_processing import NLTKEmotionAnalyzer, Text2EmotionAnalyzer, ParallelDotsEmotionAnalyzer
from tools import generate_fake_timestamps
import datetime as dt
from settings import PARALLELBOTS_API_KEY
import pandas as pd
import numpy as np
import matplotlib, os
import matplotlib.pyplot as plt # importing matplotlib
import holoviews as hv
from holoviews import opts
import plotly.express as px

hv.extension('bokeh', 'matplotlib')

matplotlib.rcParams["figure.dpi"] = 200

def main():
    paremo_obj  = ParallelDotsEmotionAnalyzer()
    path        = "C:/Users/pzin/OneDrive - Simulations Plus, Inc/Documents/HackNC/AI-Counselor-Pet/sample_today_data/"
    file        = os.path.join(path, "time_text_file.txt")

    df          = pd.read_csv(file, sep='\t')

    emotions, sentiments    = [], []

    for i in df['Text']:
        emotion_dict = paremo_obj.guess_emotion(i)['emotion']
        predicted_emotion = max(emotion_dict, key=emotion_dict.get)

        sentiment_dict    = paremo_obj.guess_sentiment(i)['sentiment']
        predicted_sentiment = max(sentiment_dict, key=sentiment_dict.get)

        emotions.append(predicted_emotion)
        sentiments.append(predicted_sentiment)

    df['Emotions']   = emotions
    df['Sentiments'] = sentiments


    output_file      = file[:-4]+'_emotions.txt'
    df.to_csv(output_file, sep='\t', index=False)

    print("\n-> Finished predicting your emotions and sentiments.")
    print("-> Now the result file can be located at ", output_file)

    df_emotion = df['Emotions'].value_counts().rename_axis('Emotion Types').reset_index(name='Counts')

    emotion_count_dict = dict(df_emotion['Emotion Types'].value_counts())
    strongest_emotion  = max(emotion_count_dict, key=emotion_count_dict.get)


    df_sentiment = df['Sentiments'].value_counts().rename_axis('Sentiment Types').reset_index(name='Counts')

    sentiment_count_dict = dict(df_sentiment['Sentiment Types'].value_counts())
    strongest_sentiment  = max(sentiment_count_dict, key=sentiment_count_dict.get)
    print('****************************************************************')
    print(f"\n\nYour feelings are mostly {strongest_sentiment} today.")
    print(f"Your strongest emotion today is {strongest_emotion}. Do you know why? The distribution of your emotions and sentiments charts will be generated soon.\n\n")
    print('****************************************************************')

    fig1 = px.bar(df_emotion, x='Emotion Types', y='Counts')
    fig1_path = os.path.join(path, 'emotion.html')
    fig1.write_html(fig1_path)

    print("-> Distribution of your emotions are here: ", fig1_path)

    fig2 = px.bar(df_sentiment, x='Sentiment Types', y='Counts')
    fig2_path = os.path.join(path, 'sentiment.html')
    fig2.write_html(fig2_path)

    print("-> Distribution of your sentiments are here: ", fig2_path)


if __name__ == '__main__':
    main()
