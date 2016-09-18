import tensorflow as tf
import numpy as np
from collections import deque
import random

# Hyper Parameters for DQN
STATE_DIM = 3           # robot state([row, col, direction])
ACTION_DIM = 3          # move_forward, turn right, turn left
GAMMA = 0.9             # discount factor for target Q
INITIAL_EPSILON = 0.5   # starting value of epsilon
FINAL_EPSILON = 0.01    # final value of epsilon
REPLAY_SIZE = 10000     # experience replay buffer size
BATCH_SIZE = 10         # size of minibatch
HIDDEN_LAYER_DIM = 200


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
        W_conv1 = self.weight_variable([3, 3, 1, 6])
        b_conv1 = self.bias_variable([6])
        W_conv2 = self.weight_variable([3, 3, 6, 10])
        b_conv2 = self.bias_variable([10])
        W_conv3 = self.weight_variable([3, 3, 10, 10])
        b_conv3 = self.bias_variable([10])
        W_fc1 = self.weight_variable([160, 32])
        b_fc1 = self.bias_variable([32])
        W_fc2 = self.weight_variable([35, 35])
        b_fc2 = self.bias_variable([35])
        W_fc3 = self.weight_variable([35, self.action_dim])
        b_fc3 = self.bias_variable([self.action_dim])

        # input layer
        self.state_input = tf.placeholder("float", [None, 10, 10, 1])
        self.state_robot = tf.placeholder("float", [None, self.state_dim])

        # hidden layers
        h_conv1 = tf.nn.relu(self.conv2d(self.state_input, W_conv1, 1) + b_conv1)
        h_conv2 = tf.nn.relu(self.conv2d(h_conv1, W_conv2, 1) + b_conv2)
        h_conv3 = tf.nn.relu(self.conv2d(h_conv2, W_conv3, 1) + b_conv3)
        h_conv3_flat = tf.reshape(h_conv3, [-1, 160])
        h_fc1 = tf.nn.relu(tf.matmul(h_conv3_flat, W_fc1) + b_fc1)

        # append robot state
        h_fc_combine = tf.concat(1, [h_fc1, self.state_robot])
        h_fc2 = tf.nn.relu(tf.matmul(h_fc_combine, W_fc2) + b_fc2)

        # Q Value layer
        self.Q_value = tf.matmul(h_fc2, W_fc3) + b_fc3

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
        state_map_batch = [data[0][0] for data in minibatch]
        state_robot_batch = [data[0][1] for data in minibatch]
        action_batch = [data[1] for data in minibatch]
        reward_batch = [data[2] for data in minibatch]
        next_state_map_batch = [data[3][0] for data in minibatch]
        next_state_robot_batch = [data[3][1] for data in minibatch]

        Q_value_batch = self.Q_value.eval(feed_dict={self.state_input: next_state_map_batch,
                                                     self.state_robot: next_state_robot_batch})

        # Step 2: calculate y
        y_batch = []
        for i in range(0, BATCH_SIZE):
            done = minibatch[i][4]
            if done:
                y_batch.append(reward_batch[i])
            else:
                y_batch.append(reward_batch[i] + GAMMA * np.max(Q_value_batch[i]))

        self.optimizer.run(feed_dict={
            self.y_input: y_batch,
            self.action_input: action_batch,
            self.state_input: state_map_batch,
            self.state_robot: state_robot_batch
        })

    def weight_variable(self, shape):
        initial = tf.truncated_normal(shape)
        return tf.Variable(initial)

    def bias_variable(self, shape):
        initial = tf.constant(0.01, shape=shape)
        return tf.Variable(initial)

    def conv2d(self, x, W, stride):
        return tf.nn.conv2d(x, W, strides=[1, stride, stride, 1], padding="VALID")

    def _append_replay_buf(self, buf):
        self.replay_buffer.append(buf)
        if len(self.replay_buffer) > REPLAY_SIZE:
            self.replay_buffer.popleft()

    def get_egreedy_action(self, state):
        Q_value = self.Q_value.eval(feed_dict={
            self.state_input: [state[0]],
            self.state_robot: [state[1]]})[0]

        # self.epsilon -= (INITIAL_EPSILON - FINAL_EPSILON) / 1000000
        if random.random() <= self.epsilon:
            action_map = [0,0,0,0,0,1,2]
            return action_map[random.randint(0, 6)]
            # return random.randint(0, self.action_dim - 1)
        else:
            # print 'DQN action probability:', self.epsilon
            return np.argmax(Q_value)

    def get_action(self, state):
        return np.argmax(self.Q_value.eval(feed_dict={
            self.state_input: [state[0]],
            self.state_robot: [state[1]]
        })[0])

    def perceive(self, state, action, reward, next_state, done):
        one_hot_action = np.zeros(self.action_dim)
        one_hot_action[action] = 1
        self._append_replay_buf((state, one_hot_action, reward, next_state, done))
        self._train_Q_network()

    def save_train_params(self):
        self.saver.save(self.session, 'algrithm/train_result')