from pico2d import *

from bird import Bird
from boy import Boy
from grass import Grass
import game_world

import game_framework


bird = None

def handle_events():
    global running

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            bird.handle_event(event)

def init():
    global bird
    global running

    running = True
    grass = Grass()
    game_world.add_object(grass, 0)

    bird = Bird()
    game_world.add_object(bird, 1)

def update():
    game_world.update()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    game_world.clear()

def pause(): pass
def resume(): pass

