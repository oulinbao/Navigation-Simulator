from ui import config


class Wall(object):
    def __init__(self):
        self._boxes = []
               
    @property
    def boxes(self):
        return self._boxes
    
class HorizonWall(Wall):
    def __init__(self, start, end):
        Wall.__init__(self)
        for i in range(start, end + 1):
            self._boxes.append(i)
            
class VerticalWall(Wall):
    def __init__(self, start, end):
        Wall.__init__(self)
        for i in range(start, end + 1, config.COL_NUM):
            self._boxes.append(i)