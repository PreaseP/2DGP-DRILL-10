from pico2d import *

from bird import Bird
from grass import Grass
import game_world

import game_framework

def handle_events():
    global running

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            for bird in birds:
                bird.handle_event(event)

def init():
    global birds
    global running

    running = True
    grass = Grass()
    game_world.add_object(grass, 0)

    birds = []

    for x in range(400, 150, -50):
        birds.append(Bird(x,100))

    for x in range(375, 125, -50):
        birds.append(Bird(x,150))

    game_world.add_objects(birds, 1)

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

