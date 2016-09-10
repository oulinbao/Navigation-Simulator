import wx
from infra.color import Color

class BoxState():
    BOX_STATE_NOT_PASS = 0
    BOX_STATE_PASSED = 1
    BOX_STATE_WALL =2


class Box(object):

    def __init__(self, panel, box_id, color, position, size):
        self._white_box = self._create_bitmap('infra/image/white.jpg')
        self._black_box = self._create_bitmap('infra/image/black.jpg')
        self._green_box = self._create_bitmap('infra/image/green.jpg')
        self._red_box = self._create_bitmap('infra/image/red.jpg')

        self.color_map = {Color.BLACK : self._black_box, 
                          Color.WHITE : self._white_box, 
                          Color.GREEN : self._green_box,
                          Color.RED   : self._red_box}

        self._bitmap = wx.StaticBitmap(panel, box_id, self.color_map[color], 
                                       pos=position, size=size)
        self._position = position
        self._box_id = box_id
        self._passed_count = 0
        
    def _create_bitmap(self, image_name):
        return wx.Image(image_name, wx.BITMAP_TYPE_JPEG).ConvertToBitmap()
    
    def change_color(self, color):
        self._bitmap.SetBitmap(self.color_map[color])
        
    def is_wall(self):
        return self._bitmap.GetBitmap() == self._black_box

    @property
    def passed_count(self):
        return self._passed_count

    @passed_count.setter
    def passed_count(self, flag):
        self._passed_count = flag

    @property
    def id(self):
        return self._box_id

    @property
    def position(self):
        return self._position