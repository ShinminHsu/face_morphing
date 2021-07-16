import numpy as np
import os
import csv
import pickle

from keras.callbacks import EarlyStopping
from keras import backend as K


def train(model, X, Y):
    
    # callback
    earlyStopping = EarlyStopping(monitor='loss', min_delta=0.0001, patience=20)
    callbacks_list = [earlyStopping]
    
    history = model.fit(
        X,
        Y, 
        batch_size=16,
        epochs=100,
        shuffle=True,
        validation_split=0,
        verbose=0,
        callbacks=callbacks_list
    )
    
    return model

        

def compute_mean_std(result_morph, result_raw, all_morph, all_raw):
    
    result_morph['cor_mean'] = np.mean(all_morph)
    result_raw['cor_mean'] = np.mean(all_raw)

    result_morph['cor_std'] = np.std(all_morph)
    result_raw['cor_std'] = np.std(all_raw)
    
    return result_morph, result_raw
    
    
def save_result(DIR_LOG, RECORD_FILE, filename, params, result_morph, result_raw):
    
    # save the result
    with open(DIR_LOG + RECORD_FILE, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=result_raw.keys())
        writer.writerow(result_morph)
        writer.writerow(result_raw)

    # save the results
    result = {
        'params': params,
        'morph': result_morph,
        'raw': result_raw
    }
        
    with open(f'{DIR_LOG}{filename}.pickle', 'wb') as f:
        pickle.dump(result, f)
    
#     print(result)
    
def check_folder_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)