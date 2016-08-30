from ui.box import Box, Color
from ui.wall import HorizonWall, VerticalWall
from ui import config


class HouseMap(object):
    
    def __init__(self, panel):
        self._boxes = []
        self._panel = panel        
    
        self.draw_base_grid(panel)  
        self.draw_house_map([HorizonWall(0, 39), VerticalWall(39, 1199), 
                             HorizonWall(1160, 1199), VerticalWall(0, 1160),
                             VerticalWall(700, 1180), VerticalWall(20, 420)])
        self.draw_target_box((4, 30))
    
    def draw_base_grid(self, panel):
        for row in range(config.ROW_NUM):
            for col in range(config.COL_NUM):
                box_id = row * config.COL_NUM + col
                position = (col*config.UNIT_WIDTH, row*config.UNIT_WIDTH)
                size = (config.UNIT_WIDTH, config.UNIT_WIDTH)
                
                box = Box(panel, box_id, Color.WHITE, position = position, size = size)
                self._boxes.append(box)

    def draw_house_map(self, walls):
        for wall in walls:
            for box_id in wall.boxes:
                box = self._boxes[box_id]
                box.change_color(Color.BLACK)
                
    def draw_target_box(self, position):
        box = self.get_box(position)
        box.change_color(Color.RED)
        
    def get_box(self, position):
        row = position[0]
        col = position[1]
        box_id = row * config.COL_NUM + col
        return self._boxes[box_id]
        