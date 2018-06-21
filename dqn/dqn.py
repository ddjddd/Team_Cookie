import numpy as np
import tensorflow as tf


class DQN:
    def __init__(self, session, input_size, output_size, name="main"):
        self.session = session
        self.input_size = input_size
        self.output_size = output_size
        self.net_name = name

        self._build_network()

    def _build_network(self, h_size=200, l_rate=1e-4):
        with tf.variable_scope(self.net_name):
            self._X = tf.placeholder(tf.float32, [None, self.input_size], name="input_x")

            # First layer of weights
            W1 = tf.get_variable("W1", shape=[self.input_size, h_size],
                                 initializer=tf.contrib.layers.xavier_initializer())
            b1 = tf.Variable(tf.random_normal([h_size]))
            layer1 = tf.nn.relu(tf.matmul(self._X, W1) + b1)

            #Second layer of Weights
            W2 = tf.get_variable("W2", shape=[h_size, h_size],
                                 initializer=tf.contrib.layers.xavier_initializer())
            b2 = tf.Variable(tf.random_normal([h_size]))
            #layer2 = tf.nn.tanh(tf.matmul(layer1, W2))
            layer2 = tf.nn.relu(tf.matmul(layer1, W2) + b2)

            W3 = tf.get_variable("W3", shape=[h_size, self.output_size], # W3가 마지막이 되었으므로 h_size를 self.output_size로 고침.
                                 initializer=tf.contrib.layers.xavier_initializer())
            b3 = tf.Variable(tf.random_normal([self.output_size]))
            # layer3 = tf.nn.relu(tf.matmul(layer2, W3) + b3)

            # W4 = tf.get_variable("W4", shape=[h_size, h_size],
            #                      initializer=tf.contrib.layers.xavier_initializer())
            # b4 = tf.Variable(tf.random_normal([h_size]))
            # layer4 = tf.nn.relu(tf.matmul(layer3, W4) + b4)
            #
            # W5 = tf.get_variable("W5", shape=[h_size, h_size],
            #                      initializer=tf.contrib.layers.xavier_initializer())
            # b5 = tf.Variable(tf.random_normal([h_size]))
            # layer5 = tf.nn.relu(tf.matmul(layer4, W5) + b5)
            #
            # W6 = tf.get_variable("W6", shape=[h_size, h_size],
            #                      initializer=tf.contrib.layers.xavier_initializer())
            # b6 = tf.Variable(tf.random_normal([h_size]))
            # layer6 = tf.nn.relu(tf.matmul(layer5, W6) + b6)
            #
            # W7 = tf.get_variable("W7", shape=[h_size, h_size],
            #                      initializer=tf.contrib.layers.xavier_initializer())
            # b7 = tf.Variable(tf.random_normal([h_size]))
            # layer7 = tf.nn.relu(tf.matmul(layer6, W7) + b7)
            #
            # W8 = tf.get_variable("W8", shape=[h_size, h_size],
            #                      initializer=tf.contrib.layers.xavier_initializer())
            # b8 = tf.Variable(tf.random_normal([h_size]))
            # layer8 = tf.nn.relu(tf.matmul(layer7, W8) + b8)

            # Last layer of Weights
            # W9 = tf.get_variable("W9", shape=[h_size, self.output_size],
            #                      initializer=tf.contrib.layers.xavier_initializer())
            # b9 = tf.Variable(tf.random_normal([self.output_size]))

            # Q prediction
            # self._Qpred = tf.matmul(layer8, W9) + b9
            self._Qpred = tf.matmul(layer2, W3) + b3

        # We need to define the parts of the network needed for learning a policy
        self._Y = tf.placeholder(shape=[None, self.output_size], dtype=tf.float32)

        # Loss function
        self._loss = tf.reduce_mean(tf.square(self._Y - self._Qpred))
        #self._loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=self._Qpred, labels=self._Y))

        # Learning
        self._train = tf.train.AdamOptimizer(learning_rate=l_rate).minimize(self._loss)

    def predict(self, state):
        x = np.reshape(state, [1, self.input_size])
        return self.session.run(self._Qpred, feed_dict={self._X: x})

    def update(self, x_stack, y_stack):
        return self.session.run([self._loss, self._train], feed_dict={self._X: x_stack, self._Y: y_stack})



