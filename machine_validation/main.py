import os
from pickle import TRUE
import numpy as np

from scipy.stats import pearsonr

from keras.models import load_model
from keras import backend as K
K.set_image_data_format('channels_last')

from input_data import load_data, save_train_test, find_subjectIDs
from models import build_cnn_model, pearson_r
from utils import train, compute_mean_std, save_result, check_folder_exists


def save_initial_models():
    """
    Save ten models with initial weights
    """
    
    for iteration in range(10):
        
        model_save_folder = os.path.join(DIR_MODEL, 'initial')
        check_folder_exists(model_save_folder)
        model_save_path = os.path.join(model_save_folder, f'{model_name}_{iteration}.h5')
        
        model = build_cnn_model(params)  # build the model
        model.save(model_save_path)  # save the model
                
        if iteration == 0:
            print(model.summary())
            

def leave_one_out(model_path, iteration):

    """
    Iterate the database using leave-one-out and load models with initial weights.
    Train and test separately on (1) morphed images + raw images (2) only raw images.
    """
    
    preds_morph, preds_raw, Y_true = [], [], []
    
    # leave one subject out
    for ID in subjectIDs:
        
        model_morph = load_model(model_path, custom_objects={'pearson_r': pearson_r})
        model_raw = load_model(model_path, custom_objects={'pearson_r': pearson_r})
                    
        # save train and test data
        X_img_train, X_img_train_raw, Y_int_train, Y_int_train_raw, X_img_test_raw, Y_int_test_raw = save_train_test(data, [ID])
        
        # train
        model_morph = train(model_morph, X_img_train, Y_int_train)  # train on morphed images + raw images
        model_raw = train(model_raw, X_img_train_raw, Y_int_train_raw)  # train on only raw images
        
        # test
        pred_morph = model_morph.predict(X_img_test_raw)
        pred_raw = model_raw.predict(X_img_test_raw)
                
        # save the prediction
        preds_morph.append(pred_morph[0][0])
        preds_morph.append(pred_morph[1][0])
        
        preds_raw.append(pred_raw[0][0])
        preds_raw.append(pred_raw[1][0])
        
        Y_true.append(Y_int_test_raw[0][0])
        Y_true.append(Y_int_test_raw[1][0])
        
                
    return preds_morph, preds_raw, Y_true
            
            
def train_test():

    """
    Train and test repeating ten times with initial weights
    """
    
    result_morph = {'type': 'morph', 'params': params}
    result_raw = {'type': 'raw', 'params': params}

    all_morph, all_raw = [], []
    
    for iteration in range(10):
        
        model_path = os.path.join(DIR_MODEL, 'initial', f'{model_name}_{iteration}.h5')
        
        preds_morph, preds_raw, Y_true = leave_one_out(model_path, iteration)
        
        cor_morph, _ = pearsonr(preds_morph, Y_true)
        cor_raw, _ = pearsonr(preds_raw, Y_true)

        print('Morph cor =', cor_morph, '\nRaw cor =', cor_raw)

        result_morph[f'cor_{iteration}'] = cor_morph
        result_raw[f'cor_{iteration}'] = cor_raw

        all_morph.append(cor_morph)
        all_raw.append(cor_raw)

    return result_morph, result_raw, all_morph, all_raw


def main():
    
    if save_model:
        save_initial_models()
        
    result_morph, result_raw, all_morph, all_raw = train_test()
    
    result_morph, result_raw = compute_mean_std(result_morph, result_raw, all_morph, all_raw)
    save_result(DIR_LOG, RECORD_FILE, model_name, params, result_morph, result_raw)
    


if __name__ == '__main__':
    
    ROOT = 'YOUR/ROOT'

    emotion = 'happy'
    MODEL_TYPE = 'cnn'
    database_path = '/WHERE/YOU/PUT/THE/DATASET'
    save_model = True  # set True if you haven't save models with initial weights first
    
    params = {
        'kernel_size': 5,
        'n_features': 32,
        'learning_rate': 0.001,
        'FC_size': 256,
        'n_pooling': 4
    }
    
    model_name = f"{MODEL_TYPE}_d{params['n_features']}_fc{params['FC_size']}_k{params['kernel_size']}"

    # paths
    DIR_LOG = ROOT + f'/WHERE/YOU/WANT/TO/STORE/RECORD/FILE/{model_name}/'
    RECORD_FILE = f'{emotion}.csv'
    DIR_MODEL = ROOT + f'models/{MODEL_TYPE}/{model_name}/'  # to store models with initial weights

    check_folder_exists(DIR_MODEL)
    check_folder_exists(DIR_LOG)
    
    # load data
    data = load_data(database_path)
    subjectIDs = find_subjectIDs(data)

    main()