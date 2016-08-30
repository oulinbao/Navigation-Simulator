import wx
from ui.wall import HorizonWall, VerticalWall
from ui import config
from ui.box import Box, Color
  
class HouseMap(wx.Frame):

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, 
                          size=(config.HOUSE_LENGTH, config.HOUSE_WIDTH))
        self.boxes = []
        panel = wx.Panel(self, -1)
        self.make_base_grid(panel)  
        self.make_house_map(panel, 
                            [HorizonWall(0, 39), VerticalWall(39, 1199), 
                             HorizonWall(1160, 1199), VerticalWall(0, 1160),
                             VerticalWall(700, 1180), VerticalWall(20, 420)])
        self.Show(True)
        
    def make_base_grid(self, panel):
        for row in range(config.ROW_NUM):
            for col in range(config.COL_NUM):
                box_id = row * config.COL_NUM + col
                box = Box(panel, box_id, Color.WHITE, 
                          position = (col*config.UNIT_WIDTH, row*config.UNIT_WIDTH),
                          size = (config.UNIT_WIDTH, config.UNIT_WIDTH))
                self.boxes.append(box)

    def make_house_map(self, panel, walls):
        for wall in walls:
            for box_id in wall.boxes:
                box = self.boxes[box_id]
                box.change_color(panel, Color.BLACK)

        
app = wx.App(False)
frame = HouseMap(None, 'House Map')
app.MainLoop()