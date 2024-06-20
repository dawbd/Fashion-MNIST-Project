# -*- coding: utf-8 -*-
"""Project-Dawson-Dinh-Fashion

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1P8qzBh8_oBPbVeMNJc08HCTYLTWjLPJY

Name: Dawson Dinh
"""

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')
from IPython import display
import pandas as pd
import tensorflow as tf
import keras
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout

from google.colab import drive
drive.mount('/content/drive')

train_path = "/content/drive/MyDrive/mlcourse/final/fashion-mnist_train.csv"
test_path = "/content/drive/MyDrive/mlcourse/final/fashion-mnist_test.csv"

train_df = pd.read_csv(train_path)
test_df = pd.read_csv(test_path)

train_df.head()

#This cell is to split the training data and testing data into X and Y arrays
train_data = np.array(train_df, dtype='float32')
test_data = np.array(test_df, dtype='float32')

x_train = train_data[:, 1:] / 255
y_train = keras.utils.to_categorical(train_data[:, 0], num_classes=10)
x_test = test_data[:, 1:] / 255
y_test = keras.utils.to_categorical(test_data[:, 0], num_classes=10)

#The dataset did not include a validation set so in this cell
#I split the training data into train and validate arrays
x_train, x_validate, y_train, y_validate = train_test_split(
    x_train, y_train, test_size=0.2, random_state=12345,
)

#just to see what an image looks like 
image = x_train[20, :].reshape((28, 28))

plt.imshow(image)
plt.show()

#This cell is to prepare the image data for training the CNN.
#This is done by reshaping the input data to an appropriate shape 
image_rows = 28
image_cols = 28
batch_size = 512
image_size = (image_rows, image_cols, 1)

x_train = x_train.reshape(x_train.shape[0], *image_size)
x_test = x_test.reshape(x_test.shape[0], *image_size)
x_validate = x_validate.reshape(x_validate.shape[0], *image_size)

print('x_train shape: {}'.format(x_train.shape))
print('x_test shape: {}'.format(x_test.shape))
print('x_validate shape: {}'.format(x_validate.shape))

"""**CNN MODEL**"""

#Our CNN model 
#You can uncomment some of the layers to see the difference in performance
#Or tune hyperparamters
model = Sequential([
    Conv2D(filters=32, kernel_size=(3,3), activation='relu', input_shape=image_size),
    MaxPooling2D(pool_size=(2,2)),
    Dropout(0.2),
    Conv2D(filters=64, kernel_size=(3,3), activation='relu'),
    MaxPooling2D(pool_size=(2,2)),
    Dropout(0.2),
    Conv2D(filters=128, kernel_size=(3,3), activation='relu'),
    Dropout(0.2),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.2),
    Dense(10, activation='softmax')
])

#Compiles the CNN model by specifying the loss function optimizer
#YOu can change the optimizer but I found Adam to be the best
model.compile(loss='categorical_crossentropy', optimizer='Adam', metrics=['accuracy'])

history = model.fit(
    x_train, y_train,
    batch_size=batch_size,
    epochs=30,
    verbose=1,
    validation_data=(x_validate, y_validate),
)

score = model.evaluate(x_test, y_test, verbose=0)
#evaluate the performance of the model after training
test_loss, test_accuracy = model.evaluate(x_test, y_test, verbose=0)
print('Test loss: {:.4f}'.format(score[0]))
print('Test accuracy: {:.4f}'.format(score[1]))

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.show()

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.show()

def plot_curves(history):
    fig, axs = plt.subplots(2, 1, figsize=(10, 10))
    axs[0].plot(history.history['accuracy'], label='Training Accuracy')
    axs[0].plot(history.history['val_accuracy'], label='Validation Accuracy')
    axs[0].set_title('Training and Validation Accuracy')
    axs[0].legend()

    axs[1].plot(history.history['loss'], label='Training Loss')
    axs[1].plot(history.history['val_loss'], label='Validation Loss')
    axs[1].set_title('Training and Validation Loss')
    axs[1].legend()

    plt.show()

plot_curves(history)