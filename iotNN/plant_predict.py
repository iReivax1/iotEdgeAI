import matplotlib.pyplot as plt
import numpy as np
import os
import PIL
import tensorflow as tf
import tensorflow_datasets as tfds
from tensorflow import keras
device_name = tf.test.gpu_device_name()
seed = 10
batch_size = 64
width = 500
height = 500
channel = 3
lr = 1e-3
epochs = 1
num_classes=3
class_list = ["bean_rust","angular_leaf_spot","healthy"]
model_dir = "/Users/xavier/Documents/NTU/CZ4171/Assignment/iotNN/bean_tf2/ibean"
# model_dir = "/home/xavi0007/iotNN/bean_tf2/ibean"
# image_dir = "/Users/xavier/Documents/NTU/CZ4171/Assignment/iotClient/healthy.png"

def load_data(): 
    ds_test, ds_info = tfds.load(
    'beans',
    split=['test'],
    shuffle_files=True,
    as_supervised=True,
    with_info=True,
    )

    return ds_test, ds_info
def preprocess(ds_test, ds_info):
    ds_test = ds_test.batch(batch_size)
    ds_test = ds_test.cache().prefetch(tf.data.experimental.AUTOTUNE)   
    return ds_test

def model_predict(model, input_image_dir):
    # results = model.evaluate(ds_test, verbose=1, batch_size=256)

    with tf.device(str(device_name)):
        img = keras.preprocessing.image.load_img(
            input_image_dir, target_size=(500, 500,3)
        )
        
        img_array = keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)
        y_pred = model.predict(img_array)
        score = tf.nn.softmax(y_pred[0])
        print(
                    "This image most likely belongs to {} with a {:.2f} percent confidence."
                    .format(class_list[np.argmax(score)], 100 * np.max(score))
                )
        a = class_list[np.argmax(score)]
        b = 100 * np.max(score)
        
        return a, b


def main(image_dir):
    # ds_test, ds_info = load_data()
    # ds_test = preprocess(ds_test,ds_info)
    saved_model = tf.keras.models.load_model(model_dir)
    print("predicting")
    a,b = model_predict(saved_model, image_dir)
    return a , b
    # print(f'the model effectiveness is, Loss :[{results[0]}]  Acc : [{results[1]}]')



if __name__ == "__main__":
    main(image_dir)