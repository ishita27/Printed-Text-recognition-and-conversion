import numpy as np
import tensorflow as tf
import random


sess = tf.Session()

def loadDataSet():
    # load the dataset
    data = np.load('data_set.npz', encoding='latin1')
    training_data = data['training_data']
    #print(len(training_data))
    validation_data = data['validation_data']
    test_data = data['testing_data']

    # format the dataset into array and output labels in one hot format
    training_inputs = [np.reshape(training_data[x]['img'],(1,1024)) for x in range(len(training_data))]
    training_results = [vectorized_result(training_data[x]['label']) for x in range(len(training_data))]
    training_data = {'training_inputs': training_inputs, 'training_results': training_results}

    validation_inputs =  [np.reshape(validation_data[x]['img'],(1,1024)) for x in range(len(validation_data))]
    validation_results = [vectorized_result(validation_data[x]['label']) for x in range(len(validation_data))]
    validation_data = {'validation_inputs': validation_inputs, 'validation_results': validation_results}
   

    test_inputs =  [np.reshape(test_data[x]['img'],(1,1024)) for x in range(len(test_data))]
    test_results = [vectorized_result(test_data[x]['label']) for x in range(len(test_data))]
    test_data = {'test_inputs': test_inputs, 'test_results': test_results}
    print(len(test_inputs))

    return [training_data, test_data, validation_data]


def vectorized_result(y):
    e = np.zeros((1,62))
    e[0][y] = 1.0
    return e


training_data, test_data,validation_data =loadDataSet()

n_hidden_1 = 2048
n_hidden_2 = 2048
n_hidden_3 = 2048
n_hidden_4 = 2048
n_classes = 62
batch_size = 10

x = tf.placeholder(tf.float32, [None, 1024])
y = tf.placeholder(tf.float32, [None, n_classes])


def neural_network_model(data):
    hidden_layer_1 = {
        'weights': tf.Variable(tf.random_normal([1024, n_hidden_1])),
        'biases': tf.Variable(tf.random_normal([n_hidden_1]))
    }

    hidden_layer_2 = {
        'weights': tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2])),
        'biases': tf.Variable(tf.random_normal([n_hidden_2]))
    }

    hidden_layer_3 = {
        'weights': tf.Variable(tf.random_normal([n_hidden_2, n_hidden_3])),
        'biases': tf.Variable(tf.random_normal([n_hidden_3]))
    }

    hidden_layer_4 = {
        'weights': tf.Variable(tf.random_normal([n_hidden_3, n_hidden_4])),
        'biases': tf.Variable(tf.random_normal([n_hidden_4]))
    }

    output_layer = {
        'weights': tf.Variable(tf.random_normal([n_hidden_4, n_classes])),
        'biases': tf.Variable(tf.random_normal([n_classes]))
    }

    layer_1 = tf.add(tf.matmul(data, hidden_layer_1['weights']), hidden_layer_1['biases'])
    tf.nn.relu(layer_1)

    layer_2 = tf.add(tf.matmul(layer_1, hidden_layer_2['weights']), hidden_layer_2['biases'])
    tf.nn.relu(layer_2)

    layer_3 = tf.add(tf.matmul(layer_2, hidden_layer_3['weights']), hidden_layer_3['biases'])
    tf.nn.relu(layer_3)

    layer_4 = tf.add(tf.matmul(layer_3, hidden_layer_4['weights']), hidden_layer_4['biases'])
    tf.nn.relu(layer_4)

    output = tf.add(tf.matmul(layer_4, output_layer['weights']), output_layer['biases'])

    return output


def train_neural_network(x):

    prediction = neural_network_model(x)
#     print("Pred :",prediction)
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=prediction, labels=y))

    optimizer = tf.train.AdamOptimizer(0.5).minimize(cost)
    correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1))
#     print("Correct:",correct)
#     print( tf.argmax(prediction, 1),"  ",tf.argmax(y, 1))
    accuracy = tf.reduce_mean(tf.cast(correct, tf.float32))
    saver = tf.train.Saver()

    n_epochs = 30

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())

        for epoch in range(n_epochs):
            epoch_loss = 0
            total_acc = 0
            total_batches = len(training_data['training_inputs']) // batch_size
            for i in range(total_batches):
                epoch_x = np.squeeze(np.array(training_data['training_inputs'][i * batch_size:(i + 1) * (batch_size)]))
                epoch_y = np.squeeze(np.array(training_data['training_results'][i * batch_size:(i + 1) * (batch_size)]))
                _, c, acc = sess.run([optimizer, cost, accuracy], feed_dict={x: epoch_x, y: epoch_y})
                epoch_loss += c
                total_acc += acc
            save_path = saver.save(sess, "./biases_weights.ckpt")
            print('Epoch ', epoch, ' completed out of ', n_epochs, 'loss : ', epoch_loss, total_acc / total_batches)
        print('optimization finished')


        test_x = np.squeeze(np.array(validation_data['validation_inputs']))
        test_y = np.squeeze(np.array(validation_data['validation_results']))
        acc = sess.run(accuracy, feed_dict={x: test_x, y: test_y})
        print("Validation Accuracy",acc)


train_neural_network(x)
