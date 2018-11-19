#This program only trains the neural network.

import mnist_loader
training_data, validation_data, test_data = mnist_loader.load_data_wrapper()

#print(list(training_data),'\n',list(validation_data),'\n',list(test_data),)

import network2

# 784 input, 30 middle and 10 output layers
net = network2.Network([1024, 30, 66], cost=network2.CrossEntropyCost)
net.large_weight_initializer()
net.SGD(training_data, 30, 10, 0.5, lmbda = 5.0, evaluation_data=validation_data, monitor_evaluation_accuracy=True,monitor_training_accuracy=True)
