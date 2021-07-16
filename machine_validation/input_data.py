import pickle
import numpy as np

def load_data(database_path):
    """
    load dataset
    
    """
    
    with open(database_path, 'rb') as f:
        data = pickle.load(f)
    
    print("samples: %i"%(len(data)))
    
    return data


def find_subjectIDs(data):

    subjectIDs = set()

    for i in range(len(data)):
        ID = data[i]['subjectID']
        subjectIDs.add(ID)
            
    return list(subjectIDs)


def save_train_test(data, test_range, img_size=128, n_categories=7):
    
    L = len(data)

    X_img_train = np.zeros([L, img_size, img_size, 1])
    X_img_train_raw = np.zeros([L, img_size, img_size, 1])
    Y_int_train = np.zeros([L, 1])
    Y_int_train_raw = np.zeros([L, 1])
    
    X_img_test_raw = np.zeros([L, img_size, img_size, 1])
    Y_int_test_raw = np.zeros([L, 1])
    
    
    valid_train = 0
    valid_train_raw = 0
    valid_test_raw = 0

    # save data corresponding to its ID
    for i in range(L):
        
        subjectID = int(data[i]['subjectID'])
        emotion = data[i]['emotion']
        database = data[i]['database']
        
        filename = data[i]['filename']
        img = data[i]['img']
        intensity = data[i]['intensity']
        
                    
        # if ID in not in test_range, then save in training data
        if subjectID not in test_range:
            X_img_train[valid_train][:,:,0] = img
            Y_int_train[valid_train] = intensity
            valid_train += 1
            
            # only save raw images
            if '100' in filename or 'neutral' in filename:
                X_img_train_raw[valid_train_raw][:,:,0] = img
                Y_int_train_raw[valid_train_raw] = intensity
                valid_train_raw += 1
                
        else:            
            # only save raw images
            if '100' in filename or 'neutral' in filename:
                X_img_test_raw[valid_test_raw][:,:,0] = img
                Y_int_test_raw[valid_test_raw] = intensity
                valid_test_raw += 1
                                    
    
    X_img_train = X_img_train[:valid_train,:]
    Y_int_train = Y_int_train[:valid_train, :]
    
    X_img_train_raw = X_img_train_raw[:valid_train_raw,:]
    Y_int_train_raw = Y_int_train_raw[:valid_train_raw, :]
        
    X_img_test_raw = X_img_test_raw[:valid_test_raw,:]
    Y_int_test_raw = Y_int_test_raw[:valid_test_raw,:]

#     print(f'Training: morph={valid_train}, raw={valid_test_raw}, Testing: {valid_test_raw}')
    
    return X_img_train, X_img_train_raw, Y_int_train, Y_int_train_raw, X_img_test_raw, Y_int_test_raw