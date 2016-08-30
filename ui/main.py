import wx
from ui.housemap import HouseMap
from ui import config
from ui.robot import Robot, Direction
import random
from time import sleep
from threading import Thread


class House(wx.Frame):

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, 
                          size=(config.HOUSE_LENGTH, config.HOUSE_WIDTH))
        self.panel = wx.Panel(self, -1)
        self.house_map = HouseMap(self.panel)
        self.robot = Robot(self.house_map, position=(2, 2), direction=Direction.EAST)
        self.Show(True)


    def start(self):
        action_map = [self.robot.move_forward, self.robot.turn_left, self.robot.move_forward, 
                      self.robot.move_forward, self.robot.turn_right, self.robot.move_forward, 
                      self.robot.move_forward, self.robot.move_forward, self.robot.move_forward]
        for i in range(0, 1000):
            action = action_map[random.randint(0, 8)]
            action()
            sleep(0.1)
            wx.CallAfter(self.panel.Refresh)
            
        
app = wx.App(False)
house = House(None, 'Robot path planning')
thread = Thread(target=house.start)
thread.start()

app.MainLoop()