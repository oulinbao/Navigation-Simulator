from abc import ABCMeta, abstractmethod
from direction import TurnType
from game import TARGET_POS

ACTION_MOVE_FORWARD = 0
ACTION_TURN_LEFT = 1
ACTION_TURN_RIGHT = 2

REWARD_DONE = 100
REWARD_ZERO = 0
REWARD_FAR = 0
REWARD_WALL = 0
REWARD_REPEAT = -1


class Command(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self):
        raise NotImplementedError


class Action(Command):
    def __init__(self, house_map):
        self._house_map = house_map
        self._src_pos = self._house_map.robot.position
        self._robot = house_map.robot

    def execute(self):
        pass


class MoveForward(Action):
    def __init__(self, house_map):
        Action.__init__(self, house_map)

    def execute(self):
        next_pos = self._move()
        self._robot.position = next_pos
        self._house_map.record_path(next_pos)

        reward, done = self._calc_reward(next_pos)
        return next_pos, reward, done

    def _move(self):
        next_box, next_pos = self._house_map.get_next_box()
        if not next_box.is_wall():
            print 'new positon', next_pos
            return next_pos
        else:
            return self._src_pos

    def _calc_reward(self, next_pos):
        if next_pos[0] < TARGET_POS[0] + 3 and next_pos[0] > TARGET_POS[0] - 3 and \
             next_pos[1] < TARGET_POS[1] + 3 and next_pos[1] > TARGET_POS[1] - 3:
            return REWARD_DONE, True

        if self._more_far(next_pos):
            return REWARD_FAR, False
        elif self._repeat(next_pos):
            return REWARD_REPEAT, False

    def _more_far(self, next_pos):
        old_distance = self._calc_distance(self._src_pos, TARGET_POS)
        new_distance = self._calc_distance(next_pos, TARGET_POS)
        return new_distance > old_distance

    def _calc_distance(self, pos1, pos2):
        result = map(lambda x, y : y - x, pos1, pos2)
        return result[0]**2 + result[1]**2

    def _repeat(self, pos):
        return self._house_map.is_repeated(pos)

class TurnLeft(Action):
    def __init__(self, house_map):
        Action.__init__(self, house_map)

    def execute(self):
        print 'turn left'
        self._robot.direction = TurnType.TURN_LEFT
        return self._src_pos, REWARD_ZERO, False


class TurnRight(Action):
    def __init__(self, house_map):
        Action.__init__(self, house_map)

    def execute(self):
        print 'turn right'
        self._robot.direction = TurnType.TURN_RIGHT
        return self._src_pos, REWARD_ZERO, False
