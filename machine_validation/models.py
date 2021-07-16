from tensorflow.keras import Model, Input
from tensorflow.keras.layers import Flatten, Conv2D, MaxPooling2D, Dropout, BatchNormalization, Activation, Dense
from tensorflow.keras.optimizers import Adam

from keras import backend as K
K.set_image_data_format('channels_last')


def pearson_r(y_true, y_pred):
    x = y_true
    y = y_pred
    mx = K.mean(x, axis=0)
    my = K.mean(y, axis=0)
    xm, ym = x - mx, y - my
    r_num = K.sum(xm * ym)
    x_square_sum = K.sum(xm * xm)
    y_square_sum = K.sum(ym * ym)
    r_den = K.sqrt(x_square_sum * y_square_sum)
    r = r_num / r_den
    return K.mean(r)


def build_cnn_model(params, class_num=1, img_size=128):
    
    #------------ parameters ------------#
    
    n_features = params['n_features']
    kernel_size = params['kernel_size']
    FC_size = params['FC_size']
    lr = params['learning_rate']
    n_pooling = params['n_pooling']
    
    #------------ model construction ------------#
    
    img_inputs = Input(shape=(img_size, img_size, 1), name='img_input')
    
    # initial the first layer
    net = Conv2D(filters=n_features, kernel_size=kernel_size, padding='same', name='conv1_1')(img_inputs)
    net = BatchNormalization()(net)
    net = Activation("relu")(net)
    net = MaxPooling2D(pool_size=n_pooling, strides=n_pooling, padding='same', name='pool1')(net)
                    
    net = Flatten()(net)
    fc_net = Dense(FC_size, activation='relu', name='fc')(net)
    out = Dense(class_num, name='fc_out')(fc_net)
    
    model = Model(inputs=img_inputs, outputs=out)
    
    #------------ Building Model ------------#
    
    adam = Adam(lr=lr, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.1)
    model.compile(loss='mean_squared_error', optimizer=adam, metrics=[pearson_r])
    
    return model


def build_model_geom(params, class_num=1):
    
    #------------ parameters ------------#
    activation_fc = 'relu'
    FC_size = params['FC_size']
    
    #------------ model construction ------------#
    
    geo_inputs = Input(shape=(1, 39), name='geometry_input')

    fc_net = Flatten()(geo_inputs)
    fc_net = Dense(FC_size, activation = activation_fc, name = 'fc1')(fc_net)
        
    out = Dense(class_num, name='fc_out')(fc_net)
    model = Model(inputs = [geo_inputs], outputs = out)
    
    
    return model