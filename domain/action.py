from abc import ABCMeta, abstractmethod
from direction import TurnType
from game import STEP

ACTION_MOVE_FORWARD = 0
ACTION_TURN_LEFT = 1
ACTION_TURN_RIGHT = 2

REWARD_DONE = 100
REWARD_ZERO = 0
REWARD_GOOD = 200
REWARD_WALL = 0
REWARD_REPEAT = 0
REWARD_NOT_FINISHED = -100


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
        self._robot.action_count += 1
        self._house_map.record_path(next_pos)

        reward, done = self._calc_reward(next_pos)
        return next_pos, reward, done

    def _move(self):
        next_box, next_pos = self._house_map.get_next_box()
        if not next_box.is_wall():
            # print 'new positon', next_pos
            return next_pos
        else:
            return self._src_pos

    def _calc_reward(self, next_pos):
        if next_pos == self._house_map.target_pos:
            return REWARD_DONE, True

        print self._robot.action_count
        if self._robot.action_count >= STEP:
            return REWARD_NOT_FINISHED, False

        return REWARD_ZERO, False


class TurnLeft(Action):
    def __init__(self, house_map):
        Action.__init__(self, house_map)

    def execute(self):
        print 'turn left'
        self._robot.direction = TurnType.TURN_LEFT
        self._robot.action_count += 1
        reward = REWARD_NOT_FINISHED if self._robot.action_count >= STEP else REWARD_ZERO
        return self._src_pos, reward, False


class TurnRight(Action):
    def __init__(self, house_map):
        Action.__init__(self, house_map)

    def execute(self):
        print 'turn right'
        self._robot.direction = TurnType.TURN_RIGHT
        self._robot.action_count += 1
        reward = REWARD_NOT_FINISHED if self._robot.action_count >= STEP else REWARD_ZERO
        return self._src_pos, reward, False
