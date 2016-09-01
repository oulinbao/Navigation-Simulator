from direction import TurnType


class Robot(object):
    def __init__(self, position, direction):
        self._position = position
        self._direction = direction

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