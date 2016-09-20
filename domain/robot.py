from actiontype import ActionType
from game import INIT_POSITION, INIT_DIRECTION


class Robot(object):

    RECORD_SIZE = 5

    def __init__(self, position, direction):
        self._position = position
        self._direction = direction
        self._action_count = 0
        self._action_record = []

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
    def direction(self, action_type):
        offset = {ActionType.ACTION_TURN_LEFT : -1, ActionType.ACTION_TURN_RIGHT : +1}
        self._direction = (self._direction + offset[action_type]) % 4

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

    def record_action(self, action_type):
        if len(self._action_record) > Robot.RECORD_SIZE:
            self._action_record.pop(0)
        self._action_record.append(action_type)

    def always_turn_around(self):
        move_count = len([x for x in self._action_record if x == ActionType.ACTION_MOVE_FORWARD])
        return move_count == 0

