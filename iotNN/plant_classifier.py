import matplotlib.pyplot as plt
import numpy as np
import os
import PIL
import tensorflow as tf
import tensorflow_datasets as tfds
from tensorflow import keras
from tensorflow.keras.layers import Input, Conv2D, BatchNormalization
from tensorflow.keras.layers import MaxPool2D, GlobalAvgPool2D
from tensorflow.keras.layers import Add, ReLU, Dense
from tensorflow.keras import Model, layers
from tensorflow.keras.callbacks import ModelCheckpoint, LearningRateScheduler
from tensorflow.keras.callbacks import ReduceLROnPlateau

'''' citation = 
@ONLINE {beansdata,
    author="Makerere AI Lab",
    title="Bean disease dataset",
    month="January",
    year="2020",
    url="https://github.com/AI-Lab-Makerere/ibean/"
}
'''
seed = 10
batch_size = 64
width = 500
height = 500
channel = 3
lr = 1e-3
epochs = 1
num_classes=3
# model_dir = "/Users/xavier/Documents/NTU/CZ4171/Assignment"
model_dir = "/home/FYP/xavi0007/iotNN"
device_name = tf.test.gpu_device_name()

def load_data(): 
    (ds_train, ds_test), ds_info = tfds.load(
    'beans',
    split=['train', 'validation'],
    shuffle_files=True,
    as_supervised=True,
    with_info=True,
    )

    return ds_train, ds_test, ds_info

def preprocess(ds_train,ds_test, ds_info):
    
    ds_train = ds_train.cache().shuffle(ds_info.splits['train'].num_examples)
    ds_train = ds_train.batch(batch_size)
    ds_train = ds_train.prefetch(tf.data.experimental.AUTOTUNE)
    
    
    ds_test = ds_test.batch(batch_size)
    ds_test = ds_test.cache().prefetch(tf.data.experimental.AUTOTUNE)
    
    return ds_train, ds_test


def lr_schedule(epoch):
    lr = 1e-3
    if epoch > 180:
        lr *= 0.5e-3
    elif epoch > 160:
        lr *= 1e-3
    elif epoch > 120:
        lr *= 1e-2
    elif epoch > 80:
        lr *= 1e-1
    print('Learning rate: ', lr)
    return lr

def model_convert_to_lite(saved_model_dir):
    # Convert the model
    converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)
    tflite_model = converter.convert()

    # Save the model.
    with open('model.tflite', 'wb') as f:
        f.write(tflite_model)

def lr_schedule(epoch):
    lr = 1e-3
    if epoch > 180:
        lr *= 0.5e-3
    elif epoch > 160:
        lr *= 1e-3
    elif epoch > 120:
        lr *= 1e-2
    elif epoch > 80:
        lr *= 1e-1
    print('Learning rate: ', lr)
    return lr


def build_model():
    model = keras.models.Sequential([
    #augmentation layers
    keras.layers.experimental.preprocessing.RandomCrop(500, 500, seed = seed, input_shape=(500,500,3)),
    keras.layers.experimental.preprocessing.RandomFlip("horizontal_and_vertical"),
    keras.layers.experimental.preprocessing.Rescaling(1./255),
    keras.layers.experimental.preprocessing.RandomRotation(0.2),
    keras.layers.experimental.preprocessing.RandomZoom(0.2),
    keras.layers.Input(shape=(500,500,3)), 
    keras.layers.Conv2D(filters=96, kernel_size=(11,11), strides=(4,4), activation='relu'),
    keras.layers.BatchNormalization(),
    keras.layers.MaxPool2D(pool_size=(3,3), strides=(2,2)),
    keras.layers.Conv2D(filters=256, kernel_size=(5,5), strides=(1,1), activation='relu', padding="same"),
    keras.layers.BatchNormalization(),
    keras.layers.MaxPool2D(pool_size=(3,3), strides=(2,2)),
    keras.layers.Conv2D(filters=384, kernel_size=(3,3), strides=(1,1), activation='relu', padding="same"),
    keras.layers.BatchNormalization(),
    keras.layers.Conv2D(filters=384, kernel_size=(1,1), strides=(1,1), activation='relu', padding="same"),
    keras.layers.BatchNormalization(),
    keras.layers.Conv2D(filters=256, kernel_size=(1,1), strides=(1,1), activation='relu', padding="same"),
    keras.layers.BatchNormalization(),
    keras.layers.MaxPool2D(pool_size=(3,3), strides=(2,2)),
    keras.layers.Flatten(),
    keras.layers.Dense(4096, activation='relu'),
    keras.layers.Dense(4096, activation='relu'),
    keras.layers.Dropout(0.5),
    keras.layers.Dense(num_classes, activation='softmax')
    ])

    return model

def model_predict(model, x_test,y_test):
    results = model.evaluate(x_test, y_test, verbose=1, batch_size=256)
    return results

def plot_graph(_history):

    acc = _history.history['accuracy']
    val_acc = _history.history['val_accuracy']
    loss = _history.history['loss']
    val_loss = _history.history['val_loss']


    plt.plot(range(1, len(loss) + 1), loss, label='Train')
    plt.plot(range(1, len(val_loss) + 1), val_loss, label='Test')
    plt.title('Model Loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend()
    filename_loss = "images/"+"_loss.png"
    plt.savefig(os.path.join(model_dir,str(filename_loss)))
    plt.close()

    # Save the plot for accuracies
    plt.plot(range(1, len(acc) + 1), acc, label='Train')
    plt.plot(range(1, len(val_acc) + 1), val_acc, label='Test')
    plt.title('Model Accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend()

    filename_acc = "images/"+"_acc.png"
    plt.savefig(os.path.join(model_dir, str(filename_acc)))
    plt.close()

def train_model(ds_train, ds_test, model):
    with tf.device(str(device_name)):
        
        
        optimizer = tf.keras.optimizers.Adam(learning_rate = lr_schedule(0))
        
    
        lr_scheduler = LearningRateScheduler(lr_schedule)

        lr_reducer = ReduceLROnPlateau(factor=np.sqrt(0.1),
                                    cooldown=0,
                                    patience=5,
                                    min_lr=0.5e-6)
        
        model.compile(optimizer=optimizer,
                    loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
                    metrics=['accuracy'])

        history = model.fit(
            ds_train,
            epochs=epochs,
            validation_data=ds_test,
            callbacks=[lr_reducer, lr_scheduler],
            verbose = 1
            )
    
    return model, history

def main():
    ds_train, ds_test, ds_info = load_data()
    print(ds_info)
    ds_train, ds_test = preprocess(ds_train,ds_test,ds_info)
    model = build_model()
    model, history = train_model(ds_train, ds_test, model)
    plot_graph(history)
    model.save(os.path.join(model_dir,str("ibean")))
    

if __name__ == "__main__":
    main()