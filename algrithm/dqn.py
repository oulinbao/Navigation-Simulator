import tensorflow as tf
import numpy as np
from collections import deque
import random

# Hyper Parameters for DQN
STATE_DIM = 3           # row, col
ACTION_DIM = 3          # move_forward, turn right, turn left
GAMMA = 0.9             # discount factor for target Q
INITIAL_EPSILON = 0.9   # starting value of epsilon
FINAL_EPSILON = 0.01    # final value of epsilon
REPLAY_SIZE = 10000     # experience replay buffer size
BATCH_SIZE = 10         # size of minibatch
HIDDEN_LAYER_DIM = 32


class DQN():
    def __init__(self):
        # init experience replay
        self.replay_buffer = deque()

        self.time_step = 0
        self.epsilon = INITIAL_EPSILON
        self.state_dim = STATE_DIM
        self.action_dim = ACTION_DIM

        self.create_Q_network()
        self.create_training_method()

        # Init session
        self.session = tf.InteractiveSession()
        try:
            self.saver = tf.train.Saver()
            self.saver.restore(self.session, 'algrithm/train_result')
        except ValueError, e:
            print e.message
            self.session.run(tf.initialize_all_variables())

    def create_Q_network(self):
        # network weights
        W1 = self.weight_variable([self.state_dim, HIDDEN_LAYER_DIM])
        b1 = self.bias_variable([HIDDEN_LAYER_DIM])
        W2 = self.weight_variable([HIDDEN_LAYER_DIM, HIDDEN_LAYER_DIM])
        b2 = self.bias_variable([HIDDEN_LAYER_DIM])
        W3 = self.weight_variable([HIDDEN_LAYER_DIM, HIDDEN_LAYER_DIM])
        b3 = self.bias_variable([HIDDEN_LAYER_DIM])
        W4 = self.weight_variable([HIDDEN_LAYER_DIM, self.action_dim])
        b4 = self.bias_variable([self.action_dim])
        # input layer
        self.state_input = tf.placeholder("float", [None, self.state_dim])
        # hidden layers
        h_layer1 = tf.nn.relu(tf.matmul(self.state_input, W1) + b1)
        h_layer2 = tf.nn.relu(tf.matmul(h_layer1, W2) + b2)
        h_layer3 = tf.nn.relu(tf.matmul(h_layer2, W3) + b3)
        # Q Value layer
        self.Q_value = tf.matmul(h_layer3, W4) + b4

    def create_training_method(self):
        self.action_input = tf.placeholder("float", [None, self.action_dim])  # one hot presentation
        self.y_input = tf.placeholder("float", [None])
        Q_action = tf.reduce_sum(tf.mul(self.Q_value, self.action_input), reduction_indices=1)
        self.cost = tf.reduce_mean(tf.square(self.y_input - Q_action))
        self.optimizer = tf.train.AdamOptimizer(1e-4).minimize(self.cost)

    def _train_Q_network(self):
        if len(self.replay_buffer) < BATCH_SIZE:
            return

        self.time_step += 1
        # Step 1: obtain random minibatch from replay memory
        minibatch = random.sample(self.replay_buffer, BATCH_SIZE)
        state_batch = [data[0] for data in minibatch]
        action_batch = [data[1] for data in minibatch]
        reward_batch = [data[2] for data in minibatch]
        next_state_batch = [data[3] for data in minibatch]

        # Step 2: calculate y
        y_batch = []
        Q_value_batch = self.Q_value.eval(feed_dict={self.state_input: next_state_batch})
        for i in range(0, BATCH_SIZE):
            done = minibatch[i][4]
            if done:
                y_batch.append(reward_batch[i])
            else:
                y_batch.append(reward_batch[i] + GAMMA * np.max(Q_value_batch[i]))

        self.optimizer.run(feed_dict={
            self.y_input: y_batch,
            self.action_input: action_batch,
            self.state_input: state_batch
        })

    def weight_variable(self, shape):
        initial = tf.truncated_normal(shape)
        return tf.Variable(initial)

    def bias_variable(self, shape):
        initial = tf.constant(0.01, shape=shape)
        return tf.Variable(initial)

    def _append_replay_buf(self, buf):
        self.replay_buffer.append(buf)
        if len(self.replay_buffer) > REPLAY_SIZE:
            self.replay_buffer.popleft()

    def get_egreedy_action(self, state):
        Q_value = self.Q_value.eval(feed_dict={self.state_input: [state]})[0]
        self.epsilon -= (INITIAL_EPSILON - FINAL_EPSILON) / 100000

        if random.random() <= self.epsilon:
            action_map = [0,0,0,0,0,1,2]
            return action_map[random.randint(0, 6)]
            # return random.randint(0, self.action_dim - 1)
        else:
            print 'select action from DQN', self.epsilon
            return np.argmax(Q_value)

    def get_action(self, state):
        return np.argmax(self.Q_value.eval(feed_dict={
            self.state_input: [state]
        })[0])

    def perceive(self, state, action, reward, next_state, done):
        one_hot_action = np.zeros(self.action_dim)
        one_hot_action[action] = 1
        self._append_replay_buf((state, one_hot_action, reward, next_state, done))
        self._train_Q_network()

    def save_train_params(self):
        self.saver.save(self.session, 'algrithm/train_result')