from .. import settings

from .Box import Box
from .Character import Character
from .Tilemap import Tile, TileMap, TILE_TEXTURE_DEF
from .Bomb import Bomb

class Scene:
    def __init__(self):
        self.tile_map = None
        self.character = None
        self.box1 = None
        self.box2 = None
        self.bomb1 = None
        self.bomb2 = None
        self.target = None
        self.__load_environment()

        self.actions_map = [
            self.move_left,
            self.move_down,
            self.move_right,
            self.move_up,
            self.push,
        ]
        self.push_directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    def __load_environment(self) -> None:
        with open(settings.ENVIRONMENT, "r") as f:
            rows, cols = f.readline().split(" ")
            rows, cols = int(rows), int(cols)
            self.tile_map = TileMap(rows, cols)

            for i in range(rows):
                row = f.readline()
                if row[-1] == "\n":
                    row = row[:-1]
                row = row.split(" ")

                for j, s in enumerate(row):
                    x, y = TileMap.to_screen(i, j)
                    self.tile_map.tiles[i][j] = Tile(x, y, TILE_TEXTURE_DEF[s], 0)
                    self.tile_map.map[i][j] = s

            row, col = f.readline().split(" ")
            row, col = int(row), int(col)
            x, y = TileMap.to_screen(row, col)
            self.character = Character(x, y, self)

            row, col = f.readline().split(" ")
            row, col = int(row), int(col)
            x, y = TileMap.to_screen(row, col)
            self.box1 = Box(x, y, self)
            self.tile_map.tiles[row][col].busy = True

            row, col = f.readline().split(" ")
            row, col = int(row), int(col)
            x, y = TileMap.to_screen(row, col)
            self.box2 = Box(x, y, self)
            self.tile_map.tiles[row][col].busy = True

            row, col = f.readline().split(" ")
            self.target = int(row), int(col)

            row, col = f.readline().split(" ")
            row, col = int(row), int(col)
            x, y = TileMap.to_screen(row, col)
            self.bomb1 = Bomb(x, y, self)
            self.tile_map.tiles[row][col].busy = False

            row, col = f.readline().split(" ")
            row, col = int(row), int(col)
            x, y = TileMap.to_screen(row, col)
            self.bomb2 = Bomb(x, y, self)
            self.tile_map.tiles[row][col].busy = False


    def reset(self):
        self.tile_map = None
        self.character = None
        self.box1 = None
        self.box2 = None
        self.bomb1 = None
        self.bomb2 = None
        self.target = None
        self.__load_environment()
        return self.get_state()

    def get_state(self):
        mc_i, mc_j = TileMap.to_map(self.character.x, self.character.y)
        mc_d = self.character.direction
        b1_i, b1_j = TileMap.to_map(self.box1.x, self.box1.y)
        b2_i, b2_j = TileMap.to_map(self.box2.x, self.box2.y)
        mc_p = mc_i * self.tile_map.cols + mc_j
        b1_p = b1_i * self.tile_map.cols + b1_j
        b2_p = b2_i * self.tile_map.cols + b2_j

        return mc_d, mc_p, b1_p, b2_p

    def apply_action(self, action):
        self.actions_map[action](action)
        return self.get_state()

    def move_right(self, action):
        self.character.move_right(action)

    def move_left(self, action):
        self.character.move_left(action)

    def move_up(self, action):
        self.character.move_up(action)

    def move_down(self, action):
        self.character.move_down(action)

    def push(self, action):
        mc_i, mc_j = TileMap.to_map(self.character.x, self.character.y)
        os_i, os_j = self.push_directions[self.character.direction]
        push_target = mc_i + os_i, mc_j + os_j
        b1_t = TileMap.to_map(self.box1.x, self.box1.y)
        b2_t = TileMap.to_map(self.box2.x, self.box2.y)

        if push_target == b1_t:
            self.box1.push(os_i, os_j)
        elif push_target == b2_t:
            self.box2.push(os_i, os_j)

    def check_win(self):
        b1 = TileMap.to_map(self.box1.x, self.box1.y)
        b2 = TileMap.to_map(self.box2.x, self.box2.y)

        win = self.target in (b1, b2)
        if(win):
            print('YOU WIN, you are the best!')

        return win
    
    def check_loses(self):
        bomb1 = TileMap.to_map(self.bomb1.x, self.bomb1.y)
        bomb2 = TileMap.to_map(self.bomb2.x, self.bomb2.y)
        characeter = TileMap.to_map(self.character.x, self.character.y)
        
        bomb1Explodes = characeter == bomb1
        bomb2Explodes = characeter == bomb2
        explosion = bomb1Explodes or bomb2Explodes
        
        if(bomb1Explodes):
            self.bomb1.explosion()
        if(bomb2Explodes):
            self.bomb2.explosion()

        if(explosion):
            self.character.life_points-=50

        isDead = self.character.life_points == 0

        if(explosion):
            print('explosion', explosion, 'isDead', isDead)
            print('life points', self.character.life_points)

        
        if(explosion and isDead):
            print("GAME OVER, your life points was reduced to cero!")
            return True
        else:
            return False
        

    def render(self, surface):
        self.tile_map.render(surface)
        surface.blit(settings.GAME_TEXTURES["switch"], TileMap.to_screen(*self.target))
        self.box1.render(surface)
        self.box2.render(surface)
        self.bomb1.render(surface)
        self.bomb2.render(surface)
        self.character.render(surface)
