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


    input_size = 6  # Size of input data in binary representation
    output_size = 1  # Output neuron

    # Initializing random weights
    np.random.seed(42)
    weights = np.random.random((input_size, output_size))

    # Training the network
    for iteration in range(iterations):
        output = sigmoid(np.dot(X_train, weights))
        error = y_train - output 

        # Backpropagation
        delta = error * sigmoid_derivative(output)
        correction = np.dot(X_train.T, delta)

        # Updating weights
        weights += correction
    
    return weights

# Testing on new data
def predict(binary_input, weights):
    output = sigmoid(np.dot(binary_input, weights))
    return round(output[0])

def nn_testing():
    iterations = [100, 1000, 10000, 50000]
    for train_vectors in range(4, 16):
        for i in range(len(iterations)):
            weights = learning(train_vectors, iterations[i])

            # Testing the network on numbers from 0 to 63
            error_cnt = 0  # Count of times the network made an error
            for j in range(64):
                binary_input = format(j, '06b')
                result = predict(np.array(list(map(int, binary_input))), weights)
                error_cnt += j % 2 != result
                #print(f"{j} (binary: {binary_input}) is {'even' if result == 0 else 'odd'}")

            print(f'Count of training vectors: {train_vectors} \nCount of iterations: {iterations[i]} \nCount of errors: {error_cnt}')
            print()

nn_testing()
