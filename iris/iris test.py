import pandas as pd
import numpy as np
import tensorflow as tf

iris = pd.read_csv('iris(150).csv', encoding='utf-8', engine='python')
iris = pd.get_dummies(iris)

maindata = iris[['SepalLength', 'SepalWidth', 'PetalLength', 'PetalWidth']]
mainname = iris[['Species_setosa', 'Species_versicolor', 'Species_virginica']]

x = tf.keras.layers.Input(shape=[4])
y = tf.keras.layers.Dense(3, activation='softmax')(x)
model = tf.keras.models.Model(x, y)
model.compile(loss='categorical_crossentropy', metrics='accuracy')

model.fit(maindata, mainname, epochs=2500)
 
print(maindata.shape, mainname.shape)

arr = np.empty((0,4), float)
arr = np.append(arr, np.array([[6.2,2.8,4.8,1.5]]), axis=0)
arr = np.append(arr, np.array([[4.5,3.1,1.4,0.3]]), axis=0)
arr = np.append(arr, np.array([[6.3,3.0,5.6,1.9]]), axis=0)
print(model.predict(arr[0:]))