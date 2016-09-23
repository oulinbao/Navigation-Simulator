from infra.color import Color


class BoxState():
    BOX_STATE_NOT_PASS = 0
    BOX_STATE_PASSED = 1
    BOX_STATE_WALL =2


class Box(object):

    def __init__(self, box_id, color, position):
        self._color = color
        self._position = position
        self._box_id = box_id
        self._passed_count = 0

    def change_color(self, color):
        self._color = color
        
    def is_wall(self):
        return self._color == Color.BLACK

    @property
    def passed_count(self):
        return self._passed_count

    @passed_count.setter
    def passed_count(self, flag):
        self._passed_count = flag

    @property
    def id(self):
        return self._box_id

    @property
    def position(self):
        return self._position