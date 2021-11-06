
from pathlib import Path 

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
            
