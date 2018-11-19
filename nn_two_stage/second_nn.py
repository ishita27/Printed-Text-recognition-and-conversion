#This program is used for giving custom user input to the NN and see the output.

import network2
import numpy as np

def get_eq_let_ijl1I(number):
	if number == 0:
		return 18
	if number == 1:
		return 19
	if number == 2:
		return 21
	if number == 3:
		return 29
	if number == 4:
		return 44
	if number == 5:
		return 47
	if number == 6:
		return 1
		

def get_eq_let_ceg(number):
	if number == 0:
		return 12
	if number == 1:
		return 14
	if number == 2:
		return 42
		
def get_let_from_2nd_nn_ijltIL1(letter):
	
	net = network2.Network([1024, 30, 7], cost=network2.CrossEntropyCost)
	
	biases_saved = np.load('nn_two_stage/biases_ijltIL1.npy',encoding='latin1')
	weights_saved = np.load('nn_two_stage/weights_ijltIL1.npy',encoding='latin1')
	
	output = np.argmax(net.feedforward(letter, biases_saved = biases_saved, weights_saved = weights_saved))
	
	return get_eq_let_ijl1I(output)

def get_let_from_2nd_nn_ceg(letter):
	
	net = network2.Network([1024, 30, 3], cost=network2.CrossEntropyCost)
	
	biases_saved = np.load('nn_two_stage/biases_ceg.npy',encoding='latin1')
	weights_saved = np.load('nn_two_stage/weights_ceg.npy',encoding='latin1')
	
	output = np.argmax(net.feedforward(letter, biases_saved = biases_saved, weights_saved = weights_saved))
	
	return get_eq_let_ceg(output)
