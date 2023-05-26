from .. import settings

from .Entity import Entity
from .Tilemap import TileMap

class Bomb(Entity):
    def __init__(self, x, y, scene):
        self.bombx = x
        self.bomby = y
        self.sc = scene
        self.isExploded = False
        super().__init__(x, y, settings.TILE_SIZE, settings.TILE_SIZE, "bomb", 0, scene)

    def explosion(self):
        if(self.isExploded != True):
            i, j = TileMap.to_map(self.x, self.y)
            self.tile_map.tiles[i][j].busy = True
            self.isExploded = True
            super().__init__(self.bombx, self.bomby, settings.TILE_SIZE, settings.TILE_SIZE, "explosion", 0, self.sc)
    

    def delete_explosion(self):
        i, j = TileMap.to_map(self.x, self.y)
        if(self.isExploded):
            self.tile_map.tiles[i][j].busy = False
            super().__init__(self.bombx, self.bomby, settings.TILE_SIZE, settings.TILE_SIZE, "ice", 0, self.sc)