# EmotionalCounselor

# A speech to text system that detects the emotion of the speaker and provides analysis and suggestions for dealing with the emotion detected.

Python Libraries Used:
- AssemblyAI
- ParallelDots
- NLTK
- pandas
- plotly
- argparse
- requests


*convert-audio-to-text.py* 
- prompts a user to choose a folder containing audio files (expects audio files to be named based on timestamps)
- converts audio files to text
- outputs a txt file (time_text_file.txt) which contains timestamps and the text extracted from the audio files (tab separated)

*predict-analyze-emotions.py* 
- based on the output file from convert-audio-to-text.py, it predicts emotions and sentiments for each text.
- The resulting files that contain predictions and sentiments are outputed in 'time_text_file_emotions.txt'
- Reveals your strongest emotion and overall sentiment throughout the day.
- Outputs two graphs: 
	- interactive 2D distribution of your emotions (exported as emotion.html)
	- interactive 2D distribution of your sentiments (exported as sentiment.html)
