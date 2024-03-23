from tensorflow.keras.datasets import mnist
import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow.keras.layers import Dense
from matplotlib.widgets import Button

# Event handler for the "Clear" button
def clear_button_callback(event):
    global drawn_digit
    drawn_digit = np.zeros((28, 28))
    ax.clear()
    ax.imshow(drawn_digit, cmap=plt.cm.binary)
    plt.draw()

# Event handler for the "Predict" button
def result_button_callback(event):
    global drawn_digit
    drawn_digit_normalized = drawn_digit / 255
    drawn_digit_expanded = np.expand_dims(drawn_digit_normalized, axis=0)
    prediction = model.predict(drawn_digit_expanded)
    predicted_digit = np.argmax(prediction)
    print("Predicted digit:", predicted_digit)

# Function to update the image while drawing
def update(event):
    global drawn_digit, mouse_pressed
    if mouse_pressed and event.xdata is not None and event.ydata is not None:
        x, y = int(round(event.xdata)), int(round(event.ydata))
        drawn_digit[y, x] = 255
        ax.clear()
        ax.imshow(drawn_digit, cmap=plt.cm.binary)
        plt.draw()

# Event handlers for mouse button
def mouse_press(event):
    global mouse_pressed
    if event.button == 1:
        mouse_pressed = True

def mouse_release(event):
    global mouse_pressed
    if event.button == 1:
        mouse_pressed = False

### Model Training ###
# Loading the dataset
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Normalization
x_train = x_train / 255
x_test = x_test / 255

# Converting to categorical format
y_train_cat = keras.utils.to_categorical(y_train, 10)
y_test_cat = keras.utils.to_categorical(y_test, 10)

# Creating the model
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)),
    Dense(100, activation='relu'),
    Dense(10, activation='softmax')
])

# Compilation
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Training
model.fit(x_train, y_train_cat, batch_size=32, epochs=10, validation_split=0.2, verbose=False)

### Drawing Digits ###
drawn_digit = np.zeros((28, 28))

mouse_pressed = False # Flag indicating mouse button pressed

# Creating a window for drawing
fig, ax = plt.subplots()
ax.imshow(drawn_digit, cmap=plt.cm.binary)
fig.canvas.mpl_connect('button_press_event', mouse_press)
fig.canvas.mpl_connect('button_release_event', mouse_release)
fig.canvas.mpl_connect('motion_notify_event', update)

# Creating buttons
ax_clear = plt.axes([0.85, 0.01, 0.1, 0.05])
ax_result = plt.axes([0.7, 0.01, 0.15, 0.05])
btn_clear = Button(ax_clear, 'Clear')
btn_result = Button(ax_result, 'Result')
btn_clear.on_clicked(clear_button_callback)
btn_result.on_clicked(result_button_callback)

plt.show()
