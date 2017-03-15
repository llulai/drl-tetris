from keras.models import Model
from keras.layers import Input, Dense, Convolution2D, Flatten
from keras.optimizers import RMSprop


def create_model(lr=.001):

    main_input = Input(shape=(20, 10, 1))
    cnn = Convolution2D(8, 3, 3, border_mode='same', activation='relu')(main_input)
    cnn = Convolution2D(16, 3, 3, border_mode='same', activation='relu')(cnn)
    cnn = Convolution2D(32, 3, 3, border_mode='same', activation='relu')(cnn)
    cnn = Flatten()(cnn)
    cnn = Dense(64, init='normal', activation='sigmoid')(cnn)
    cnn = Dense(32, init='normal', activation='sigmoid')(cnn)

    value = Dense(4, init='normal')(cnn)

    model = Model(input=main_input, output=value)

    model.compile(optimizer=RMSprop(lr=lr), loss='mse')

    return model