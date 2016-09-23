from domain.game import Game
from domain.housemap import HouseMap

if __name__ == '__main__':
    house_map = HouseMap()
    game = Game(house_map)
    game.play()