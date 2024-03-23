import numpy as np

# Activation function
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Derivative of the activation function
def sigmoid_derivative(x):
    return x * (1 - x)


def learning(n, iterations):
    X_train = np.zeros((n, 6), dtype=int)  # Training dataset, built automatically based on the argument n
    y_train = np.zeros((1, n), dtype=int)  # Training set response vector, also built automatically
    
    for i in range(n):
        binary_str = format(i, '06b')
        for j in range(6):
            X_train[i, j] = int(binary_str[j])
        y_train[0][i] = i % 2
    y_train = y_train.T


    # Creating a neural network with one hidden layer
    input_size = 6  # Input data size 
    hidden_size = 2  # Number of neurons in the hidden layer
    output_size = 1  # Output neuron

    # Initializing random weights
    np.random.seed(42)
    weights_input = np.random.random((input_size, hidden_size))  # Weights used at the input of the hidden layer
    weights_output = np.random.random((hidden_size, output_size))  # Weights at the output of the hidden layer

    # Training the network
    for iteration in range(iterations):

        # Forward propagation
        layer1_input = np.dot(X_train, weights_input)
        layer1_output = sigmoid(layer1_input)
        layer2_input = np.dot(layer1_output, weights_output)
        layer2_output = sigmoid(layer2_input)

        # Error calculation
        error = y_train - layer2_output

        # Backpropagation
        delta_output = error * sigmoid_derivative(layer2_output)
        error_layer1 = delta_output.dot(weights_output.T)
        delta_layer1 = error_layer1 * sigmoid_derivative(layer1_output)

        # Updating weights
        weights_output += layer1_output.T.dot(delta_output) 
        weights_input += X_train.T.dot(delta_layer1)
    
    return weights_input, weights_output


def predict(binary_input, weights_input, weights_output):
    hidden_input = np.dot(binary_input, weights_input)
    hidden_output = sigmoid(hidden_input)
    output_input = np.dot(hidden_output, weights_output)
    output = sigmoid(output_input)
    return round(output[0])

def nn_testing():
    iterations = [100, 1000, 5000, 10000]
    for train_vectors in range(3, 8):
        for i in range(len(iterations)):
            weights_input, weights_output = learning(train_vectors, iterations[i])

            # Testing the network on numbers from 0 to 63
            error_cnt = 0  # Count of times the network made an error
            for j in range(64):
                binary_input = format(j, '06b')
                result = predict(np.array(list(map(int, binary_input))), weights_input, weights_output)
                error_cnt += j % 2 != result
                #print(f"{j} (binary: {binary_input}) is {'even' if result == 0 else 'odd'}")

            print(f'Count of training vectors: {train_vectors} \nCount of iterations: {iterations[i]} \nCount of errors: {error_cnt}')
            print()

nn_testing()
