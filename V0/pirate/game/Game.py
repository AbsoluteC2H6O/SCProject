import pygame
from . import settings
from .src.Scene import Scene
import time
class Game:
    def __init__(self, title, render_mode):
        self.render_mode = render_mode

        self.scene = Scene(render_mode)

        if self.render_mode is not None:
            pygame.init()
            pygame.display.init()
            pygame.mixer.music.play(loops=-1)
            pygame.mixer.music.set_volume(0.2)
            w, h = self.scene.tile_map.width, self.scene.tile_map.height

            self.render_surface = pygame.Surface((w, h))
            self.screen = pygame.display.set_mode((w * 4, h * 4))
            pygame.display.set_caption(title)

    def reset(self):
        return self.scene.reset()

    def get_state(self):
        return self.scene.get_state()

    def update(self, action):
        new_state = self.scene.apply_action(action)
        loses = self.scene.check_loses()
        win = self.scene.check_win() 

        if(loses == True):
            if(self.render_mode is not None):
                settings.SOUNDS['lose'].play()
                time.sleep(4)
            return new_state, loses
        
        if(win == True):
            if(self.render_mode is not None):
                settings.SOUNDS['win'].play()
                time.sleep(4)
            return new_state, win
        else:
            return new_state, win
        
    def render(self):
        if self.render_mode is None:
            return

        self.render_surface.fill((0, 0, 0))

        self.scene.render(self.render_surface)

        self.screen.blit(
            pygame.transform.scale(self.render_surface, self.screen.get_size()), (0, 0)
        )

        pygame.event.pump()
        pygame.display.update()

    def close(self):
        if self.render_mode is None:
            return
        
        pygame.display.quit()
        pygame.mixer.music.stop()
