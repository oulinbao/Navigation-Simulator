import wx
from threading import Thread, Condition
from domain.game import Game
from domain.housemap import HouseMap
from infra import config


class HouseFrame(wx.Frame):

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title,
                          size=(config.HOUSE_LENGTH, config.HOUSE_WIDTH))
        self.panel = wx.Panel(self, -1)
        self._house_map = HouseMap(self.panel, self)
        thread = Thread(target=self.start)
        thread.start()
        self.Show(True)

    def refresh(self, show_type):
        self._house_map.show_robot()
        self._house_map.show_repeated()
        self.SetTitle(show_type)
        self.panel.Refresh()

    def reset(self):
        self._house_map.reset_house_map()
        self._house_map.show_robot()
        print 'reset finished in frame!'

    def start(self):
        game = Game(self, self._house_map)
        game.play()

if __name__ == '__main__':
    app = wx.App(False)
    house = HouseFrame(None, 'Robot path planning')
    app.MainLoop()