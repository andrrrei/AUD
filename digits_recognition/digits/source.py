# распознавание цифр
from tensorflow.keras.datasets import mnist
import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow.keras.layers import Dense

(x_train, y_train), (x_test, y_test) = mnist.load_data()  # загрузка выборки

# далее отображение первых 25 изображений из обучающей выборки - можно убрать
plt.figure(figsize=(10,5))
for i in range(25):
    plt.subplot(5,5,i+1)
    plt.xticks([])
    plt.yticks([])
    plt.imshow(x_train[100+i], cmap=plt.cm.binary)
plt.show()

# это самое главное, это сеть. здесь можно менять
model = keras.Sequential([
    keras.layers.Flatten (input_shape=(28, 28, 1)), # потому что размер изображения 28*28
    Dense(100, activation='relu'),
    Dense(10, activation='softmax')])
print(model.summary())     # вывод структуры НС в консоль

x_train = x_train / 255 # нормализация
x_test = x_test / 255
y_train_cat = keras.utils.to_categorical(y_train, 10) # приведение к вектору из 0 и 1 (10 - размерность)
y_test_cat = keras.utils.to_categorical(y_test, 10)

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(x_train, y_train_cat, batch_size=32, epochs=10, validation_split=0.2,  verbose=False) #обучение
model.evaluate(x_test, y_test_cat,verbose=False )
n = 5  # изображение - это номер в наборе данных
x = np.expand_dims(x_test[n], axis=0)
# выведем рукописную цифру с заданным номером, полученное сетью значение - в виде числа и в виде вектора
res = model.predict(x)

print(res, '  - такая цифра должна быть на рисунке. Верно?')
print(np.argmax(res))
plt.imshow(x_test[n], cmap=plt.cm.binary)
plt.show()

# выделение неверных результатов
pred = model.predict(x_test)
pred = np.argmax(pred, axis=1)

mask = pred == y_test
# подсчет ошибок
er = 0
for k in mask:
   if k == 0:
       er += 1
print('k-vo  error ', er)       
x_false = x_test[~mask]
y_false = x_test[~mask]
print('вывод ошибочных некоторых результатов')
print('смотрим, правильные ли ошибочные картинки, хорошо ли нарисованы')
for i in range(5):
  print("Значение сети: " + str(y_test[i]))
  plt.imshow(x_false[i], cmap = plt.cm.binary)
  plt.show()
