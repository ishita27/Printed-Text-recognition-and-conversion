#This program is used for giving custom user input to the NN and see the output.

from get_equivalent_letter import get_letter

# import mnist_loader
# training_data, validation_data, test_data = mnist_loader.load_data_wrapper()

import network2
import numpy as np
from nn_two_stage.second_nn import get_let_from_2nd_nn_ijltIL1
from nn_two_stage.second_nn import get_let_from_2nd_nn_ceg
'''from traing import loadModel
from traing import getResult'''

def get_string_from_nn(all_letters):
	net = network2.Network([1024, 30, 66], cost=network2.CrossEntropyCost)

	biases_saved = np.load('./training_nn/biases_weights/biases.npy',encoding='latin1')
	weights_saved = np.load('./training_nn/biases_weights/weights.npy',encoding='latin1')

	#all_letters = np.load('all_letters.npy')
	#all_letters = all_letters.tolist()

	word_string = ""

	#pred=loadModel()

	i = 0
	for x in all_letters:
		output = np.argmax(net.feedforward(x, biases_saved = biases_saved, weights_saved = weights_saved))
                #output = np.argmax(getResult(all_letters,pred))

		#second stage classification below
		if (output in (18, 19, 21, 29, 44, 47, 1)):
			output = get_let_from_2nd_nn_ijltIL1(x)
		elif (output in (12, 14, 42)):
			output = get_let_from_2nd_nn_ceg(x)

		word_string = word_string + get_letter(output)
		i = i + 1

	return word_string

	#print np.argmax(net.feedforward(test_data[502][0], biases_saved = biases_saved, weights_saved = weights_saved))
