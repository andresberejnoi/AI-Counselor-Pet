from pathlib import Path 
import os
from collections import defaultdict 
import pandas as pd
import datetime as dt

reference_identifiers_dict = {
    'modality': {
        '01':'full-AV',
        '02':'video-only',
        '03':'audio-only'
    },
    'vocal_channel': {'01':'speech', '02':'song'},
    'emotion':{
        '01':'neutral',
        '02':'calm',
        '03':'happy',
        '04':'sad',
        '05':'angry',
        '06':'fearful',
        '07':'disgust',
        '08':'surprised'
    },
    'emotional_intensity':{'01':'normal', '02':'strong'},
    'statement':{
        '01':"Kids are talking by the door",
        '02':"Dogs are sitting by the door"
    },
    'repetition':{'01':'1st repetition','02':'2nd repetition'},
    'actor': {f"{i:02}":'male' if i % 2==1 else 'female' for i in range(1,25)},    #I could have made it simpler, but this has an actual key for every value. Odd numbers are labeled 'male' and even values are labeled 'female'
    #'actor':{0:'female', 1:'male'},
}

def get_identifier_by_idx(filename, idx):
    path = Path(filename)
    base_name = path.stem 

    str_id = base_name.split('-')[idx]
    return str_id

def get_extension_from_filename(filename):
    path = Path(filename)
    ext  = path.suffix
    return ext

def get_vocal_channel_from_filename(filename):
    voc_chan_id = get_identifier_by_idx(filename, 1)
    return reference_identifiers_dict['vocal_channel'][voc_chan_id]

def get_emotion_from_filename(filename):
    emo_id = get_identifier_by_idx(filename, 2)
    return reference_identifiers_dict['emotion'][emo_id]

def get_intensity_from_filename(filename):
    intensity_id = get_identifier_by_idx(filename, 3)
    return reference_identifiers_dict['emotional_intensity'][intensity_id]

def get_statement_from_filename(filename):
    statement_id = get_identifier_by_idx(filename, 4)
    return reference_identifiers_dict['statement'][statement_id]

def get_repetition_from_filename(filename):
    rep_id = get_identifier_by_idx(filename, 5)
    return reference_identifiers_dict['repetition'][rep_id]

def get_actor_id_from_fileame(filename):
    str_id = get_identifier_by_idx(filename, -1)  #the last item is the actor id
    return int(str_id)

def parse_RAVDESS_filename(filename):
    '''Parse filenames from RAVDESS audio file'''

    all_files_dict = {}

    #for _name in filename_list:
    _path = Path(filename)
    extension = _path.suffix
    base_name = _path.stem
    split_identifiers = base_name.split('-')
    filename_data = {'extension':extension}

    for i, identifier in enumerate(split_identifiers):
        if i==0:
            filename_data['modality'] = reference_identifiers_dict['modality'][identifier]
        elif i==1:
            filename_data['vocal_channel'] = reference_identifiers_dict['vocal_channel'][identifier]
        elif i==2:
            filename_data['emotion'] = reference_identifiers_dict['emotion'][identifier]
        elif i==3:
            filename_data['emotional_intensity'] = reference_identifiers_dict['emotional_intensity'][identifier]
        elif i==4:
            filename_data['statement'] = reference_identifiers_dict['statement'][identifier]
        elif i==5:
            filename_data['repetition'] = reference_identifiers_dict['repetition'][identifier]
        elif i==6:
            filename_data['gender'] = reference_identifiers_dict['actor'][identifier]
            filename_data['actor_id'] = int(identifier)

    #all_files_dict[filename_data['actor_id']] = filename_data

    return filename_data
            

def get_all_file_info_dicts(data_root='./datasets'):
    '''In this lazy route, I will assume that the data is subdivided into 
    different categories (emotions)'''
    dict_for_df = defaultdict(list)    #this is a sort of dictionary that will default it's values to lists
    all_info_dicts = []
    all_dir_files = os.scandir(data_root)
    for _dir in all_dir_files:
        sub_folder = _dir.name
        #print(f"Current file object `{sub_folder}` is dir? -> {os.path.isdir(sub_folder)}")
        sub_path = os.path.join(data_root, sub_folder)
        if os.path.isdir(sub_path):
            #sub_path = os.path.join(data_root, sub_folder)
            #print(f"About to enter into sub-folder {sub_path}")
            for dir_file in os.scandir(sub_path):
                filename = dir_file.name
                file_info_dict = parse_RAVDESS_filename(filename)
                file_info_dict['path'] = os.path.join(sub_path, filename)
                #print(f".-> adding file {filename} to all_info_dicts")
                all_info_dicts.append(file_info_dict)

    return all_info_dicts

def create_df_from_dataset(data_root='./datasets', dataset='ravdess'):
    all_info_dicts = get_all_file_info_dicts(data_root)

    #code for merging dictionaries taken from StackOverflow answer here: https://stackoverflow.com/questions/5946236/how-to-merge-multiple-dicts-with-same-key-or-different-key
    dict_for_df = defaultdict(list)

    for d in all_info_dicts: # you can list as many input dicts as you want here
        for key, value in d.items():
            dict_for_df[key].append(value)

    df = pd.DataFrame(dict_for_df)
    return df

def generate_fake_timestamps(num_stamps, time_spacing):
    '''
    time_spacing: int, float
        The number of hours in between timestamps
    '''
    stamps = []
    time_delta = dt.timedelta(hours=time_spacing)
    start_time = dt.datetime.now()    #uses local time, not UTC
    start_time = start_time.replace(hour=9) 
    start_time = start_time.replace(minute=30) 

    stamps.append(start_time)
    for i in range(1, num_stamps):
        start_time += time_delta
        stamps.append(start_time)

    return stamps

