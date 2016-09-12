from abc import ABCMeta, abstractmethod
from direction import TurnType
from reward import RewardCalculator, REWARD_ZERO
from game import MAX_STEP

ACTION_MOVE_FORWARD = 0
ACTION_TURN_LEFT = 1
ACTION_TURN_RIGHT = 2


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

    def _calc_reward(self, next_pos):
        if self._robot.action_count == MAX_STEP or self._house_map.is_all_covered():
            calculator = RewardCalculator(self._house_map.calculate_coverage_rate(),
                                          self._house_map.calculate_repeat_rate(),
                                          self._robot.action_count)
            return calculator.calculate()
        return REWARD_ZERO


class MoveForward(Action):
    def __init__(self, house_map):
        Action.__init__(self, house_map)

    def execute(self):
        next_pos = self._move()
        # print next_pos
        self._robot.position = next_pos
        self._robot.action_count += 1

        return next_pos, self._calc_reward(next_pos), self._house_map.is_all_covered()

    def _move(self):
        next_box, next_pos = self._house_map.get_next_box()
        if not next_box.is_wall():
            self._house_map.record_footprint(next_pos)
            return next_pos
        else:
            return self._src_pos


        # if self._house_map.just_passed(next_pos):
        #     return 1
        # else:
        #     return -1


class TurnLeft(Action):
    def __init__(self, house_map):
        Action.__init__(self, house_map)

    def execute(self):
        # print 'left'
        self._robot.direction = TurnType.TURN_LEFT
        self._robot.action_count += 1
        return self._src_pos, self._calc_reward(self._src_pos), False


class TurnRight(Action):
    def __init__(self, house_map):
        Action.__init__(self, house_map)

    def execute(self):
        # print 'right'
        self._robot.direction = TurnType.TURN_RIGHT
        self._robot.action_count += 1
        return self._src_pos, self._calc_reward(self._src_pos), False
