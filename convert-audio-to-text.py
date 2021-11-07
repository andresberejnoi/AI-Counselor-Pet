#-------------------------------------------------------------------------------
# Name:        convert-audio-to-text.py
# Purpose:     Convert audio files in a folder to text and output a csv file containing time-stamps and the detected text.
#
# Author:      pzin
#
# Created:     06/11/2021
# Copyright:   (c) pzin 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import sys, os, argparse
import time
import requests
import pandas as pd
from tkinter import Tk, filedialog

def read_file(filename, chunk_size=5242880):
    with open(filename, 'rb') as _file:
        while True:
            data = _file.read(chunk_size)
            if not data:
                break
            yield data

def check_status(endpoint, response, headers):
    '''
    check status at every 0.5 s.
    '''
    status = response.json()['status']
    while status == 'queued' or status == 'failed' or status == 'processing':
        time.sleep(0.5)
        response = requests.get(endpoint, headers=headers)
        status = response.json()['status']
    else:
        return status, response

def speech_to_text(audio_file_path):

    '''
    Given an audio file, the function will return the text.
    '''

    headers = {
            "authorization": "API_KEY",
            "content-type": "application/json"
        }


    upload_url_response = requests.post('https://api.assemblyai.com/v2/upload',
                         headers=headers,
                         data=read_file(audio_file_path))


    # Get the transcription result.
    endpoint = "https://api.assemblyai.com/v2/transcript"

    json = {
      "audio_url": upload_url_response.json()['upload_url']
    }

    id_response = requests.post(endpoint, json=json, headers=headers)

    # perhaps standing in the queue

    transcription_id  = id_response.json()['id']
    endpoint = "https://api.assemblyai.com/v2/transcript/" + transcription_id
    id_response = requests.get(endpoint, headers=headers)
    status = id_response.json()['status']
    status_result, id_response = check_status(endpoint, id_response, headers)

    # if status is completed, fetch the results
    if status_result == 'completed':
        text_result = id_response.json()['text']
        return audio_file_path, text_result
    else:
        return audio_file_path, 'Not Successful.'


##def command_line_interface():
##    parser = argparse.ArgumentParser(description= "")
##    parser.add_argument('-i', '--inputfolder', type=str, help="Put the name of the folder containing audio files.")
##    # args = parser.parse_args()
##    args, unknown = parser.parse_known_args()
##    return args

def extract_filename(file):
    ext_index = file.rfind('.')
    filename  = file[:ext_index]
    return filename

def check_if_name_exists_in_time_to_text_file(name_of_interest, time_to_text_file):
    '''
    Check if the current file name exists in the time column of time_to_text_file.
    If it exists, return True. If not, return False.
    '''
    df = pd.read_csv(time_to_text_file, sep='\t')
    time_stamps = [extract_filename(name) for name in df['Time']]
    if name_of_interest in time_stamps:
        return True
    else:
        return False


def main():
    # path = 'C:/Users/pzin/OneDrive - Simulations Plus, Inc/Documents/HackNC/AI-Counselor-Pet/preprocessed_datasets/ravdess_dataset/speech/Actor_01/'
    root = Tk() # pointing root to Tk() to use it as Tk() in program.
    root.withdraw() # Hides small tkinter window.

    root.attributes('-topmost', True) # Opened windows will be active. above all windows despite of selection.
    path          = filedialog.askdirectory()

    files_in_path = [i for i in os.listdir(path) if '.csv' not in i]

    #    filename = "03-01-01-01-01-02-01.wav"
    time_text_file = os.path.join(path, 'time_text_file.csv')

    if not os.path.exists(time_text_file):
        with open(time_text_file, 'w') as f:
            f.write('Time\tText\n ')
            f.close()

    with open(time_text_file, 'a+') as f:
        for file in files_in_path:
            filename  = extract_filename(file)
            file_exists = check_if_name_exists_in_time_to_text_file(filename, time_text_file)
            if file_exists == False:
                start_time = time.time()
                file, text = speech_to_text(os.path.join(path, file))
                print(text)
                print("--- %s seconds ---" % (time.time() - start_time))
                to_write = filename+'\t'+text+'\n'
                f.write(to_write)
        f.close()

if __name__ == '__main__':
    main()