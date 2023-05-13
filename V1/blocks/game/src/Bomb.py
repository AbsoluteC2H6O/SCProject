from .. import settings

from .Entity import Entity
from .Tilemap import TileMap

class Bomb(Entity):
    def __init__(self, x, y, scene):
        self.bombx = x
        self.bomby = y
        self.sc = scene
        super().__init__(x, y, settings.TILE_SIZE, settings.TILE_SIZE, "bomb", 0, scene)

    def explosion(self):
        i, j = TileMap.to_map(self.x, self.y)

        self.tile_map.tiles[i][j].busy = True
        super().__init__(self.bombx, self.bomby, settings.TILE_SIZE, settings.TILE_SIZE, "explosion", 0, self.sc)