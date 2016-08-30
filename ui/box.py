import wx

class Box(object):

    def __init__(self, panel, box_id, color, position, size):
        self.white_box = self.create_box('white.jpg')
        self.black_box = self.create_box('black.jpg')
        self.green_box = self.create_box('green.jpg')
        self.color_map = {Color.BLACK : self.black_box, 
                          Color.WHITE : self.white_box, 
                          Color.GREEN : self.green_box}

        self.bitmap = wx.StaticBitmap(panel, box_id, self.color_map[color], pos=position, size=size)
        
    def create_box(self, image_name):
        return wx.Image(image_name, wx.BITMAP_TYPE_JPEG).ConvertToBitmap()
    
    def change_color(self, panel, color):
        self.bitmap.SetBitmap(self.color_map[color])

class Color():
    WHITE = 'white'
    BLACK = 'black'
    GREEN = 'green' 