from direction import TurnType
from game import INIT_POSITION, INIT_DIRECTION


class Robot(object):
    def __init__(self, position, direction):
        self._position = position
        self._direction = direction
        self._action_count = 0

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, pos):
        self._position = pos

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, turn_type):
        offset = {TurnType.TURN_LEFT : -1, TurnType.TURN_RIGHT : +1}
        self._direction = (self._direction + offset[turn_type]) % 4

    @property
    def action_count(self):
        return self._action_count

    @action_count.setter
    def action_count(self, count):
        self._action_count += 1

    def reset(self):
        self._position = INIT_POSITION
        self._direction = INIT_DIRECTION
        self._action_count = 0

    @property
    def init_state(self):
        return [INIT_POSITION[0], INIT_POSITION[1], INIT_DIRECTION]

    @property
    def current_state(self):
        return [self._position[0], self._position[1], self._direction]