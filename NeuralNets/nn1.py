#
# Neural Networks 101
# From: https://realpython.com/python-ai-neural-network/
#

import numpy as np

# Used in second vectors
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_deriv(x):
    return sigmoid(x) * (1-sigmoid(x))

def make_prediction(input_vector, weights, bias):
    layer_1 = np.dot(input_vector, weights) + bias
    layer_2 = sigmoid(layer_1)
    return layer_2

target = 0 # Second target, first is 1

# First section vectors
input_vector = [1.72, 1.23]
weights_1 = [1.26, 0]
weights_2 = [2.17, 0.32]

# Simple pure Pyton method to calc dot product
first_indexes_mult = input_vector[0] * weights_1[0]
second_indexes_mult = input_vector[1] * weights_1[1]

dot_product_1 = first_indexes_mult + second_indexes_mult

print(f"The Python dot product is: {dot_product_1}")

# NumPy method
dot_product_1 = np.dot(input_vector, weights_1)

print(f"The NumPy vec 1 & weight 1 dot product is: {dot_product_1}")

dot_product_2 = np.dot(input_vector, weights_2)

print(f"The NumPy vec 1 & weight 2 dot product is: {dot_product_2}")
print('-' * 10)

#
# New (second) vectors
input_vector = np.array([1.66, 1.56])
weights_1 = np.array([1.45, -0.66])

bias = np.array([0.0])

# In this case prediction is Layer 2
prediction = make_prediction(input_vector, weights_1, bias)

print(f"The prediction result is: {prediction}")

# Changing the value of input_vector
input_vector = np.array([2, 1.5])
prediction = make_prediction(input_vector, weights_1, bias)
print(f"The prediction result is: {prediction}")

mse = np.square(prediction - target)
print(f"Prediction: {prediction}; Error: {mse}")

derivative = 2 * (prediction - target)
print(f"The derivative is {derivative}")

# Updating the weights
weights_1 = weights_1 - derivative
prediction = make_prediction(input_vector, weights_1, bias)
error = (prediction - target) ** 2
print(f"Prediction: {prediction}; Error: {error}")

derror_dprediction = 2 * (prediction - target)
layer_1 = np.dot(input_vector, weights_1) + bias
dprediction_dlayer1 = sigmoid_deriv(layer_1)
dlayer1_dbias = 1
derror_dbias = (derror_dprediction * dprediction_dlayer1 * dlayer1_dbias)
