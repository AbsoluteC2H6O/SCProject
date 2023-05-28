from .. import settings
from .Character import Character
from .Tilemap import Tile, TileMap, TILE_TEXTURE_DEF
from .Bomb import Bomb

class Scene:
    def __init__(self,render_mode):
        self.tile_map = None
        self.character = None
        self.bomb1 = None
        self.bomb1IsExploded = False
        self.target = None
        self.render_mode = render_mode
        self.moves_number = 0
        self.__load_environment()

        self.actions_map = [
            self.move_left,
            self.move_down,
            self.move_right,
            self.move_up,
            self.putBomb,
        ]
        self.putBomb = [(0, -1), (1, 0), (0, 1), (-1, 0)]

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
            self.target = int(row), int(col)

    def reset(self):
        self.tile_map = None
        self.character = None
        self.bomb1 = None
        self.target = None
        self.__load_environment()
        return self.get_state()

    def get_state(self):
        mc_i, mc_j = TileMap.to_map(self.character.x, self.character.y)
        mc_d = self.character.direction
        mc_p = mc_i * self.tile_map.cols + mc_j

        return mc_d, mc_p

    def apply_action(self, action):
        self.actions_map[action](action)
        return self.get_state()

    def move_right(self, action):
        ch_x = (self.character.x//16)+1
        ch_y = (self.character.y//16)
        print('ch_x',ch_x, ch_y)
        if(self.tile_map.map[ch_x][ch_y] == 'I'):
            self.character.move_right(action)

    def move_left(self, action):
        ch_x = (self.character.x//16)-1
        ch_y = (self.character.y//16)
        print('ch_x',ch_x, ch_y)

        if(self.tile_map.map[ch_x][ch_y] == 'I'):
            self.character.move_left(action)

    def move_up(self, action):
        ch_x = self.character.x//16
        ch_y = (self.character.y//16) -1
        print('ch_x',ch_x, ch_y)

        if(self.tile_map.map[ch_x][ch_y] == 'I'):
            self.character.move_up(action)

    def move_down(self, action):
        ch_x = (self.character.x//16)
        ch_y = (self.character.y//16)+1
        print('ch_x',ch_x, ch_y)

        if(self.tile_map.map[ch_x][ch_y] == 'I'):
            self.character.move_down(action)

    def putBomb(self, action):
        self.moves_number+=1
        # print('put bomb', action)

    def check_win(self):
        ch = TileMap.to_map(self.character.x, self.character.y)

        win = self.target in (ch)
 
        return win
    
    def check_loses(self):
        isDead = self.character.life_points == 0

        if(isDead or self.moves_number ==10):
            print("GAME OVER, your life points was reduced to cero!")
            return True
        else:
            return False
        

    def render(self, surface):
        self.tile_map.render(surface)
        surface.blit(settings.GAME_TEXTURES["switch"], TileMap.to_screen(*self.target))
        self.character.render(surface)

        # Fondo del texto
        for _ in range(9):
            surface.blit(
                settings.GAME_TEXTURES['ice'],
                (_*16,
                    144)
            )
        for _ in range(9):
            surface.blit(
                settings.GAME_TEXTURES['ice'],
                (_*16,
                    160)
            )

        # Texto Life points
        font = settings.FONTS['short']
        text_obj = font.render(f"{settings.LIFE_POINTS}", True, (0, 0, 0))
        text_rect = text_obj.get_rect()
        text_rect.center = (64, 152)
        surface.blit(text_obj, text_rect)

        # Renderizado de la vida del pirata
        if(self.character.life_points > 50):
            surface.blit(
                settings.GAME_TEXTURES['life100'],
                (96, 144)
            )

        elif(self.character.life_points <= 50 and self.character.life_points > 0):
            surface.blit(
                settings.GAME_TEXTURES['life50'],
                (96, 144)
            )
        
        else:
            surface.blit(
                settings.GAME_TEXTURES['life0'],
                (96, 144)
            )

        # Texto del copy
        font = settings.FONTS['short-1']
        text_obj = font.render(f"{settings.COPY}", True, (0, 0, 0))
        text_rect = text_obj.get_rect()
        text_rect.center = (72, 166)
        surface.blit(text_obj, text_rect)