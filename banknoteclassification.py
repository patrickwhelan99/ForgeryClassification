# -*- coding: utf-8 -*-
"""bankNoteClassification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RdCMAN0NILQnR02KCiJ9ko9_Zbkux5FD
"""

import tensorflow as tf
import pandas as pd
from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt

BATCH_SIZE=128

!wget -O "data_banknote_authentication.txt" https://raw.githubusercontent.com/patrickwhelan99/ForgeryClassification/master/data_banknote_authentication.txt
!head "data_banknote_authentication.txt"

dataFrame = pd.read_csv("data_banknote_authentication.txt", names=["variance", "skew", "curtosis", "entropy", "classification"])

target = dataFrame.pop('classification')

dataset = tf.data.Dataset.from_tensor_slices((dataFrame.values, target.values))

train_dataset = dataset.shuffle(len(dataFrame)).batch(1024)

for feat, targ in train_dataset.take(10):
  print ('Features: {}, Target: {}'.format(feat, targ))

def get_compiled_model():
  model = tf.keras.Sequential([
    tf.keras.layers.Dense(10, activation='relu', dtype='float64'),
    tf.keras.layers.Dense(10, activation='relu', dtype='float64'),
    tf.keras.layers.Dense(1, activation='sigmoid', dtype='float64')
  ])

  model.compile(optimizer='adam',
                loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
                metrics=['accuracy'])
  return model

model = get_compiled_model()

history = model.fit(train_dataset, batch_size=BATCH_SIZE, epochs=200)

plt.plot(history.history['accuracy'], label='accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.ylim([history.history['accuracy'][0], 1])
plt.legend(loc='lower right')

model.evaluate(train_dataset, batch_size=BATCH_SIZE)