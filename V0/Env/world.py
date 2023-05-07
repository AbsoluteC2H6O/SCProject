import pygame

from . import settings
from .tilemap import TileMap


class World:
    def __init__(self, title, state, action, matrix, walls, initState):
        # pygame.init()
        # pygame.display.init()
        # settings.SOUNDS['game-init'].play()
        # pygame.mixer.music.play(loops=-1, fade_ms=7000)
        # self.render_surface = pygame.Surface(
        #     (settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT)
        # )
        # self.screen = pygame.display.set_mode(
        #     (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)
        # )
        # pygame.display.set_caption(title)
        self.current_state = state
        self.current_action = action
        self.render_character = True
        self.render_goal = True
        self.tilemap = None
        self.finish_state = None
        self.matrix = matrix
        self.walls = walls
        self.initState = initState
        self._create_tilemap()

    def _create_tilemap(self):
        tile_texture_names = ["metal" for _ in range(settings.NUM_TILES)]
        specialStates = [0, ((settings.ROWS*settings.COLS)-1),((settings.ROWS*settings.COLS))-settings.COLS]
        i = len(specialStates)
        for _ in range(settings.ROWS*settings.COLS):
            if (_ < settings.COLS and (_,_+1) not in self.walls and(_+1,_) not in self.walls):
                tile_texture_names[_] = "uWall"
            if (_ >= (specialStates[1]-settings.COLS) and _ < specialStates[1] and (_,_+1) not in self.walls and(_+1,_) not in self.walls):
                tile_texture_names[_] = "bWall"
            if ((_+1) % settings.ROWS == 0 and( _+1) != settings.ROWS):
                specialStates.insert(i, _)
                if(_,_-settings.ROWS) in self.walls or (_-settings.ROWS,_) in self.walls:
                    tile_texture_names[_] = "urWall"
                else:
                    tile_texture_names[_] = "rWall"
                i += 1
            if (_ % settings.ROWS == 0):
                specialStates.insert(i, _)
                if(_,_-settings.ROWS) in self.walls or (_-settings.ROWS,_) in self.walls:
                    tile_texture_names[_] = "ulWall"
                else:
                    tile_texture_names[_] = "lWall"
                i += 1
            tile_texture_names[settings.ROWS-1] = "urWall"
            
        tile_texture_names[specialStates[2]] = "lbWall"
        for state in self.walls:
            # Esquinas diagonales
            if ((0, 1) in self.walls and (0, 16) in self.walls):
                tile_texture_names[0] = "urWall"
            else:
                tile_texture_names[0] = "ulWall"
            # No considerar estados de lso bordes
            if ((specialStates[1]-1, specialStates[1]) in self.walls and (specialStates[1]-settings.ROWS, specialStates[1]) in self.walls):
                tile_texture_names[specialStates[1]] = "urbWall"
            else:
                tile_texture_names[specialStates[1]] = "brWall"
            # Rutina para impresion de muros del contenido del laberinto, para
            # ambos pares de muros en self.walls.
            if (state[0] - state[1] < 0 and state[0] not in specialStates and state[1] not in specialStates):
                if (self.isRWall(state[0], state[1])):
                    tile_texture_names[state[0]] = "rWall"
                if (self.isUWall(state[0], state[1])):
                    tile_texture_names[state[0]] = "uWall"
                if (self.isRUWall(state[0], state[1])):
                    tile_texture_names[state[0]] = "urWall"
                if (state[0] < settings.COLS and self.isRWall(state[0], state[1])):
                    tile_texture_names[state[0]] = "urWall"

                if (state[0] >= ((settings.ROWS*settings.COLS)-1-settings.COLS) and self.isRWall(state[0], state[1])):
                    tile_texture_names[state[0]] = "brWall"
            elif (state[0] not in specialStates and state[1] not in specialStates):
                if (self.isRWall(state[1], state[0])):
                    tile_texture_names[state[1]] = "rWall"
                if (self.isUWall(state[1], state[0])):
                    tile_texture_names[state[1]] = "uWall"
                if (self.isRUWall(state[1], state[0])):
                    tile_texture_names[state[1]] = "urWall"
                if (state[1] < settings.COLS and self.isRWall(state[1], state[0])):
                    tile_texture_names[state[1]] = "urWall"
                if (state[1] > ((settings.ROWS*settings.COLS)-settings.COLS) and self.isRWall(state[1], state[0])):
                    tile_texture_names[state[1]] = "brWall"
        for _, actions_table in self.matrix.items():
            for _, possibilities in actions_table.items():
                for _, state, reward, terminated in possibilities:
                    if terminated:
                        if reward > 0:
                            self.finish_state = state
                        else:
                            tile_texture_names[state] = "explosion"


        tile_texture_names[self.finish_state] = "metal"
        self.tilemap = TileMap(tile_texture_names)

    def isRWall(self, state, stateNext):
        return state + 1 == stateNext

    def isUWall(self, state, stateNext):
        return state - settings.COLS == stateNext

    def isRUWall(self, state, stateNext):
        condition = (self.isRWall(state, stateNext) and ((state, state-settings.COLS) in self.walls or (state-settings.COLS, state) in self.walls)
                     ) or (self.isUWall(state, stateNext) and ((state, state+1) in self.walls) or (state+1, state) in self.walls)
        return condition

    def reset(self, state, action):
        self.state = state
        self.action = action
        self.render_character = True
        self.render_goal = True
        for tile in self.tilemap.tiles:
            if tile.texture_name == "explosion":
                tile.texture_name = "baterry-lost-point"

    def update(self, state, action, reward, terminated):
        if terminated:
            if state == self.finish_state:
                self.render_goal = False
                # settings.SOUNDS["win"].play()
            else:
                self.tilemap.tiles[state].texture_name = "explosion"
                self.render_character = False
                # settings.SOUNDS["lost-battery"].play()
                # settings.SOUNDS["lost-game"].play()

        self.state = state
        self.action = action

    def render(self):
        # self.render_surface.fill((0, 0, 0))

        # self.tilemap.render(self.render_surface)
        # self.render_surface.blit(
        #     settings.TEXTURES["spacecraft"],
        #     (self.tilemap.tiles[self.initState].x,
        #      self.tilemap.tiles[self.initState].y),
        # )

        # if self.render_goal:
        #     self.render_surface.blit(
        #         settings.TEXTURES["baterry-charge"],
        #         (
        #             self.tilemap.tiles[self.finish_state].x,
        #             self.tilemap.tiles[self.finish_state].y,
        #         ),
        #     )

        # if self.render_character:
        #     self.render_surface.blit(
        #         settings.TEXTURES["character"][self.action],
        #         (self.tilemap.tiles[self.state].x,
        #          self.tilemap.tiles[self.state].y),
        #     )

        # self.screen.blit(
        #     pygame.transform.scale(self.render_surface,
        #                            self.screen.get_size()), (0, 0)
        # )

        # pygame.event.pump()
        # pygame.display.update()
        c=0

    def close(self):
        # pygame.mixer.music.stop()
        # pygame.mixer.quit()
        # pygame.display.quit()
        # pygame.quit()
        c=0
