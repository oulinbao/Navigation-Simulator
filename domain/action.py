from abc import ABCMeta, abstractmethod
from direction import TurnType
from game import TARGET_POS

ACTION_MOVE_FORWARD = 0
ACTION_TURN_LEFT = 1
ACTION_TURN_RIGHT = 2

REWARD_DONE = 10
REWARD_NEAR = 1
REWARD_ZERO = 0
REWARD_FAR = -1


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
        if next_pos == TARGET_POS:
            return REWARD_DONE, True

        if self._more_near(next_pos):
            return REWARD_NEAR, False
        elif self._not_move(next_pos):
            return REWARD_ZERO, False
        else:
            return REWARD_FAR, False

    def _more_near(self, next_pos):
        old_distance = self._calc_distance(self._src_pos, TARGET_POS)
        new_distance = self._calc_distance(next_pos, TARGET_POS)
        print 'old dist:', old_distance, ' new dist:', new_distance
        return new_distance < old_distance

    def _not_move(self, next_pos):
        return self._src_pos == next_pos

    def _calc_distance(self, pos1, pos2):
        result = map(lambda x, y : y - x, pos1, pos2)
        return result[0]**2 + result[1]**2


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
