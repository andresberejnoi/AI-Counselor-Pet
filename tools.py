
def parse_RAVDESS_filenames(filename_list):
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
        'actor': {i:'male' if i % 2==1 else 'female' for i in range(1,25)}    #I could have made it simpler, but this has an actual key for every value. Odd numbers are labeled 'male' and even values are labeled 'female'
    }

    filename_data = {}

    for _name in filename_list:
        split_identifiers = _name.split('-')

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

    return filename_data
            
