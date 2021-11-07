'''NLP-related code will go here'''
import nltk
from tools import get_identifier_by_idx, parse_RAVDESS_filename
import pandas as pd
import os

from collections import defaultdict


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


                