from ui.box import Color


class Robot(object):

    def __init__(self, house_map, position, direction):
        self._position = position
        self._direction = direction
        self._house_map = house_map
        
        self._show_current_position()
        
    def _show_current_position(self):
        box = self._house_map.get_box(self._position)
        box.change_color(Color.GREEN)
    
    # move setp = 1
    def move_forward(self):
        delta = {Direction.EAST  : (0, 1),
                 Direction.SOUTH : (1, 0),
                 Direction.WEST  : (0, -1),
                 Direction.NORTH : (-1, 0)}
        self._prev_position = self._position
        
        next_pos = map(lambda x,y:x+y, self._position, delta[self._direction])
        box = self._house_map.get_box(next_pos)
        if not box.is_wall():
            self._position = next_pos
            print 'new positon', self._position
            self._show_current_position()
        
    def turn_right(self):
        print 'turn right'
        self._direction = (self._direction + 1) % 4
    
    def turn_left(self):
        print 'turn left'
        self._direction = (self._direction - 1) % 4
        


class Direction():
    EAST = 0
    SOUTH = 1
    WEST = 2
    NORTH = 3