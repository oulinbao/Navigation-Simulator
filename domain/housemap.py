from box import Box
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
        self._walls = [HorizonWall(0, 39), VerticalWall(39, 1199),
                       HorizonWall(1160, 1199), VerticalWall(0, 1160),
                       VerticalWall(700, 1180), VerticalWall(20, 420)]
        self._draw_house(panel)

    @property
    def robot(self):
        return self._robot

    def _draw_house(self, panel):
        self._draw_base_grid(panel)
        self._draw_walls(self._walls)
        self._draw_target_box(TARGET_POS)

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

    def _draw_target_box(self, position):
        box = self.get_box(position)
        box.change_color(Color.RED)

    def reset_house_map(self):
        self._reset_base_grid()
        self._draw_walls(self._walls)
        self._draw_target_box(TARGET_POS)

    def _reset_base_grid(self):
        for box in self._boxes:
            box.change_color(Color.WHITE)

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
        return [next_pos[0], next_pos[1], self._robot.direction], reward, done

    def show_robot(self, position):
        box = self.get_box(position)
        box.change_color(Color.GREEN)

    def reset(self):
        wx.CallAfter(self._frame.reset)
        time.sleep(0)  # release cpu time
        with self._frame.condition:
            self._frame.condition.wait()
            self._robot = Robot(INIT_POSITION, Direction.EAST)

        print 'env reset ok'
        return [INIT_POSITION[0], INIT_POSITION[1], INIT_DIRECTION]
