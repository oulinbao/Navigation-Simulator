from box import Box, BoxState
from wall import HorizonWall, VerticalWall
from robot import Robot
from action import *
from game import INIT_DIRECTION, INIT_POSITION
from direction import Direction
from infra import config
from infra.color import Color
from abc import ABCMeta, abstractmethod
import wx
import time


class ENV(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def accept(self, action_type):
        raise NotImplementedError

    @abstractmethod
    def reset(self):
        raise NotImplementedError


class HouseMap(ENV):
    def __init__(self, panel, frame):
        self._boxes = []
        self._panel = panel
        self._frame = frame
        self._robot = Robot(INIT_POSITION, Direction.EAST)
        self._walls = [HorizonWall(0, 9), VerticalWall(9, 99),
                       HorizonWall(90, 99), VerticalWall(0, 99),
                       VerticalWall(43, 73), VerticalWall(5, 45), VerticalWall(57, 77)]
        self._draw_house(panel)

    @property
    def robot(self):
        return self._robot

    def _draw_house(self, panel):
        self._draw_base_grid(panel)
        self._draw_walls(self._walls)

    def _draw_base_grid(self, panel):
        for row in range(config.ROW_NUM):
            for col in range(config.COL_NUM):
                box_id = row * config.COL_NUM + col
                position = (col * config.UNIT_WIDTH, row * config.UNIT_WIDTH)
                size = (config.UNIT_WIDTH, config.UNIT_WIDTH)

                box = Box(panel, box_id, Color.WHITE, position=position, size=size)
                self._boxes.append(box)

    def _draw_walls(self, walls):
        for wall in walls:
            for box_id in wall.boxes:
                box = self._boxes[box_id]
                box.change_color(Color.BLACK)

    def reset_house_map(self):
        self._reset_base_grid()
        self._draw_walls(self._walls)
        self._reset_robot()

    def _reset_base_grid(self):
        for box in self._boxes:
            box.change_color(Color.WHITE)
            box.passed_count = 0

    def _reset_robot(self):
        self._robot.reset()

    def get_box(self, position):
        row = position[0]
        col = position[1]
        box_id = row * config.COL_NUM + col
        return self._boxes[box_id]

    def get_next_box(self):
        offset = {Direction.EAST: (0, 1),
                  Direction.SOUTH: (1, 0),
                  Direction.WEST: (0, -1),
                  Direction.NORTH: (-1, 0)}

        next_pos = map(lambda x, y: x + y, self._robot.position, offset[self._robot.direction])
        return self.get_box(next_pos), next_pos

    def accept(self, action_type):
        action_map = {ACTION_MOVE_FORWARD: MoveForward(self),
                      ACTION_TURN_LEFT: TurnLeft(self),
                      ACTION_TURN_RIGHT: TurnRight(self)}
        action = action_map[action_type]
        next_pos, reward, done = action.execute()
        return self._robot.current_state + self._collect_current_state(), \
            reward, done

    def show_robot(self):
        box = self.get_box(self._robot.position)
        box.change_color(Color.GREEN)

    def show_repeated(self):
        box = self.get_box(self._robot.position)
        if box.passed_count > 1:
            box.change_color(Color.RED)

    def reset(self):
        wx.CallAfter(self._frame.reset)
        time.sleep(1)  # release cpu time
        print 'env reset ok'
        return self._robot.init_state + self._collect_current_state()

    def _collect_current_state(self):
        # [index, state{0:not pass, 1:passed, 2:wall}, ....]
        state = []
        for box in self._boxes:
            state.append(box.id)
            if box.is_wall():
                state.append(BoxState.BOX_STATE_WALL)
            elif box.passed_count == 0:
                state.append(BoxState.BOX_STATE_NOT_PASS)
            else:
                state.append(BoxState.BOX_STATE_PASSED)
        return state

    def record_footprint(self, pos):
        box = self.get_box(pos)
        box.passed_count += 1

    def just_passed(self, pos):
        box = self.get_box(pos)
        return box.passed_count == 1

    def calculate_repeat_rate(self):
        return 0 if self._covered_count() == 0 else float(self._repeated_count()) / self._covered_count()

    def calculate_coverage_rate(self):
        return float(self._covered_count()) / self._all_availabe_count()

    def is_all_covered(self):
        return self._covered_count() == self._all_availabe_count()

    def _all_availabe_count(self):
        return len([box for box in self._boxes if not box.is_wall()])

    def _covered_count(self):
        return self._cal_count(0)

    def _repeated_count(self):
        return self._cal_count(1)

    def _cal_count(self, pass_count):
        return len([box for box in self._boxes if box.passed_count > pass_count])


