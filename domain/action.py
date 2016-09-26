from abc import ABCMeta, abstractmethod
from actiontype import ActionType
from reward import RewardCalculator, REWARD_ZERO
from domain.game import MAX_STEP


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

    def _calc_stop_reward(self):
        # if self._robot.always_turn_around():
        #     return -10
        return -0.5


class MoveForward(Action):
    def __init__(self, house_map):
        Action.__init__(self, house_map)

    def execute(self):
        next_pos = self._move()

        # print next_pos
        self._robot.position = next_pos
        self._robot.action_count += 1
        self._robot.record_action(ActionType.ACTION_MOVE_FORWARD)

        return next_pos, self._calc_reward(next_pos) + self._calc_hitwall_reward(next_pos), \
            self._house_map.is_all_covered()

    def _move(self):
        next_box, next_pos = self._house_map.get_next_box()
        if not next_box.is_wall():
            self._house_map.record_footprint(next_pos)
            return next_pos
        else:
            # print 'hit wall'
            return self._src_pos

    def _calc_repeat_reward(self, pos):
        box = self._house_map.get_box(pos)
        if box.passed_count > 1:
            return -0.1
        return 0

    def _calc_hitwall_reward(self, next_pos):
        if self._src_pos == next_pos:
            return -0.8
        return 0


class TurnLeft(Action):
    def __init__(self, house_map):
        Action.__init__(self, house_map)

    def execute(self):
        # print 'left'
        self._robot.direction = ActionType.ACTION_TURN_LEFT
        self._robot.action_count += 1
        self._robot.record_action(ActionType.ACTION_TURN_LEFT)

        return self._src_pos, self._calc_reward(self._src_pos) + self._calc_stop_reward(), False


class TurnRight(Action):
    def __init__(self, house_map):
        Action.__init__(self, house_map)

    def execute(self):
        # print 'right'
        self._robot.direction = ActionType.ACTION_TURN_RIGHT
        self._robot.action_count += 1
        self._robot.record_action(ActionType.ACTION_TURN_RIGHT)

        return self._src_pos, self._calc_reward(self._src_pos) + self._calc_stop_reward(), False
