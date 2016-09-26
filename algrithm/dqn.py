import tensorflow as tf
import numpy as np
from collections import deque
import random
from domain.direction import Direction
from domain.actiontype import ActionType

# Hyper Parameters for DQN
STATE_DIM = 2           # robot state([row, col])
ACTION_DIM = 4          # move_forward, right, left, back
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
        W_conv1 = self.weight_variable([3, 3, 1, 16])
        b_conv1 = self.bias_variable([16])
        W_conv2 = self.weight_variable([3, 3, 16, 32])
        b_conv2 = self.bias_variable([32])
        W_conv3 = self.weight_variable([3, 3, 32, 64])
        b_conv3 = self.bias_variable([64])
        W_conv4 = self.weight_variable([3, 3, 64, 128])
        b_conv4 = self.bias_variable([128])
        W_fc1 = self.weight_variable([512, 256])
        b_fc1 = self.bias_variable([256])
        W_fc2 = self.weight_variable([258, 128])
        b_fc2 = self.bias_variable([128])
        W_fc3 = self.weight_variable([128, 64])
        b_fc3 = self.bias_variable([64])
        W_fc4 = self.weight_variable([64, 32])
        b_fc4 = self.bias_variable([32])
        W_fc5 = self.weight_variable([32, self.action_dim])
        b_fc5 = self.bias_variable([self.action_dim])

        # input layer
        self.state_input = tf.placeholder("float", [None, 10, 10, 1])
        self.state_robot = tf.placeholder("float", [None, self.state_dim])

        # hidden layers
        h_conv1 = tf.nn.relu(self.conv2d(self.state_input, W_conv1, 1) + b_conv1)
        h_conv2 = tf.nn.relu(self.conv2d(h_conv1, W_conv2, 1) + b_conv2)
        h_conv3 = tf.nn.relu(self.conv2d(h_conv2, W_conv3, 1) + b_conv3)
        h_conv4 = tf.nn.relu(self.conv2d(h_conv3, W_conv4, 1) + b_conv4)
        h_conv4_flat = tf.reshape(h_conv4, [-1, 512])
        h_fc1 = tf.nn.relu(tf.matmul(h_conv4_flat, W_fc1) + b_fc1)

        # append robot state
        h_fc_combine = tf.concat(1, [h_fc1, self.state_robot])
        h_fc2 = tf.nn.relu(tf.matmul(h_fc_combine, W_fc2) + b_fc2)
        h_fc3 = tf.nn.relu(tf.matmul(h_fc2, W_fc3) + b_fc3)
        h_fc4 = tf.nn.relu(tf.matmul(h_fc3, W_fc4) + b_fc4)

        # Q Value layer
        self.Q_value = tf.matmul(h_fc4, W_fc5) + b_fc5

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
            action_map = [ActionType.E,ActionType.N,ActionType.S,ActionType.W]
            return action_map[random.randint(0, 3)]
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

    def get_horizon_action(self, robot_state):
        position = (robot_state[0], robot_state[1])
        direction = robot_state[2]

        action_map = {Direction.EAST:ActionType.ACTION_MOVE_FORWARD,
                      Direction.WEST: ActionType.ACTION_MOVE_FORWARD}

        if position in [(1,8),(3,8),(5,8),(7,8)]:
            action_map = {Direction.EAST:ActionType.ACTION_TURN_RIGHT,
                          Direction.SOUTH:ActionType.ACTION_MOVE_FORWARD}

        if position in [(2,8),(4,8),(6,8),(8,8)]:
            action_map = {Direction.WEST:ActionType.ACTION_MOVE_FORWARD,
                          Direction.SOUTH:ActionType.ACTION_TURN_RIGHT}

        if position in [(2,1),(4,1),(6,1),(8,1)]:
            action_map = {Direction.WEST:ActionType.ACTION_TURN_LEFT,
                          Direction.SOUTH:ActionType.ACTION_MOVE_FORWARD}

        if position in [(3,1),(5,1),(7,1),(9,1)]:
            action_map = {Direction.EAST:ActionType.ACTION_MOVE_FORWARD,
                          Direction.SOUTH:ActionType.ACTION_TURN_LEFT}

        return action_map[direction]

    def get_vertical_action(self, robot_state):
        position = (robot_state[0], robot_state[1])
        direction = robot_state[2]

        action_map = {Direction.SOUTH: ActionType.ACTION_MOVE_FORWARD,
                      Direction.NORTH: ActionType.ACTION_MOVE_FORWARD}

        if position in [(1, 1)]:
            action_map = {Direction.EAST: ActionType.ACTION_TURN_RIGHT,
                          Direction.SOUTH: ActionType.ACTION_MOVE_FORWARD}

        if position in [(8, 1), (8, 3), (8, 5), (8, 7)]:
            action_map = {Direction.EAST: ActionType.ACTION_MOVE_FORWARD,
                          Direction.SOUTH: ActionType.ACTION_TURN_LEFT}

        if position in [(8, 2), (8, 4), (8, 6), (8, 8)]:
            action_map = {Direction.EAST: ActionType.ACTION_TURN_LEFT,
                          Direction.NORTH: ActionType.ACTION_MOVE_FORWARD}

        if position in [(1, 2), (1, 4), (1, 6), (1, 8)]:
            action_map = {Direction.NORTH: ActionType.ACTION_TURN_RIGHT,
                          Direction.EAST: ActionType.ACTION_MOVE_FORWARD}

        if position in [(1, 3), (1, 5), (1, 7), (1, 9)]:
            action_map = {Direction.EAST: ActionType.ACTION_TURN_RIGHT,
                          Direction.SOUTH: ActionType.ACTION_MOVE_FORWARD}

        return action_map[direction]