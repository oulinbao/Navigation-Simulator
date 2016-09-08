from box import Box
from wall import HorizonWall, VerticalWall
from robot import Robot
from action import *
from direction import Direction
from infra import config
from infra.color import Color
from abc import ABCMeta, abstractmethod
from game import INIT_POSITION, INIT_DIRECTION
import wx
import time
import random



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
        self._target_pos = [8, 8]
        self._robot = Robot(INIT_POSITION, Direction.EAST)
        self._walls = [HorizonWall(0, 9), VerticalWall(9, 99),
                       HorizonWall(90, 99), VerticalWall(0, 99),
                       VerticalWall(43, 73), VerticalWall(5, 45), VerticalWall(67, 87)]
        self._draw_house(panel)

    @property
    def robot(self):
        return self._robot

    @property
    def target_pos(self):
        return self._target_pos

    def _draw_house(self, panel):
        self._draw_base_grid(panel)
        self._draw_walls(self._walls)
        self._draw_target_box(self._target_pos)

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
        self._draw_target_box(self._target_pos)
        self._reset_robot()

    def _reset_base_grid(self):
        for box in self._boxes:
            box.change_color(Color.WHITE)
            box.pass_through = False

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
        return [next_pos[0], next_pos[1], self._robot.direction, self._target_pos[0], self._target_pos[1]], \
               reward, done

    def show_robot(self, position):
        box = self.get_box(position)
        box.change_color(Color.GREEN)

    def reset(self):
        wx.CallAfter(self._frame.reset)
        time.sleep(1)  # release cpu time
        print 'env reset ok'
        return [INIT_POSITION[0], INIT_POSITION[1], INIT_DIRECTION, self._target_pos[0], self._target_pos[1]]

    def record_path(self, pos):
        box = self.get_box(pos)
        box.pass_through = True

    def reset_target_pos(self):
        pos = self._get_next_pos()
        box = self.get_box(pos)
        while box.is_wall():
            pos = self._get_next_pos()
            box = self.get_box(pos)
        self._target_pos = pos

    def _get_next_pos(self):
        return [random.randint(0, 9), random.randint(0, 9)]
