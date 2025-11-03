import random

from pico2d import load_image, get_time, load_font
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT

import game_world
import game_framework
from ball import Ball
from state_machine import StateMachine


def space_down(e): # e is space down ?
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

time_out = lambda e: e[0] == 'TIMEOUT'

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

# 새의 크기
PIXEL_PER_METER = (1.0 / 0.03)

bird_width = 184 # 552cm -> 약 5.5m
bird_height = 169 # 507cm -> 약 5m

# 새의 속도
RUN_SPEED_MPS = 20
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# 날개짓 속도
TIME_PER_ACTION =  1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 14


class Idle:

    def __init__(self, boy):
        self.boy = boy

    def enter(self, e):
        self.boy.wait_time = get_time()
        self.boy.dir = 0


    def exit(self, e):
        if space_down(e):
            self.boy.fire_ball()


    def do(self):
        self.boy.frame = (self.boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        if get_time() - self.boy.wait_time > 3:
            self.boy.state_machine.handle_state_event(('TIMEOUT', None))

    def draw(self):
        if self.boy.face_dir == 1: # right
            self.boy.image.clip_draw(int(self.boy.frame) * 100, 300, 100, 100, self.boy.x, self.boy.y)
        else: # face_dir == -1: # left
            self.boy.image.clip_draw(int(self.boy.frame) * 100, 200, 100, 100, self.boy.x, self.boy.y)


class Sleep:

    def __init__(self, boy):
        self.boy = boy

    def enter(self, e):
        pass

    def exit(self, e):
        pass

    def do(self):
        self.boy.frame = (self.boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8


    def handle_event(self, event):
        pass

    def draw(self):
        if self.boy.face_dir == 1:
            self.boy.image.clip_composite_draw(int(self.boy.frame)* 100, 300, 100, 100, 3.141592/2, '', self.boy.x - 25, self.boy.y - 25, 100, 100)
        else:
            self.boy.image.clip_composite_draw(int(self.boy.frame) * 100, 200, 100, 100, -3.141592/2, '', self.boy.x + 25, self.boy.y - 25, 100, 100)

bird_sprites = []

for i in range(0,5):
    for j in range(2,-1, -1):
        if i == 4 and j == 0:
            continue
        bird_sprites.append((i * bird_width, j * bird_height))

bird_dict = {1 : '', -1 : 'h'}

class Run:
    def __init__(self, bird):
        self.bird = bird

    def enter(self, e):
        pass

    def exit(self, e):
        if space_down(e):
            self.bird.fire_ball()

    def do(self):
        self.bird.frame = (self.bird.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 14
        self.bird.x += self.bird.dir * RUN_SPEED_PPS * game_framework.frame_time
        if self.bird.x < 0:
            self.bird.dir = 1
            self.bird.face_dir = 1
            self.bird.x = 0
        if self.bird.x > 1600:
            self.bird.dir = -1
            self.bird.face_dir = -1
            self.bird.x = 1600


    def draw(self):
        self.bird.image.clip_composite_draw(bird_sprites[int(self.bird.frame)][0],
                                            bird_sprites[int(self.bird.frame)][1], bird_width, bird_height,
                                            0, bird_dict[self.bird.face_dir], self.bird.x, self.bird.y, 75, 75)

class Bird:
    def __init__(self, x = 400, y = 100):

        self.item = None
        self.x, self.y = x, y
        self.frame = random.randint(0,13)
        self.face_dir = 1
        self.dir = 1
        self.image = load_image('bird_animation.png')

        self.IDLE = Idle(self)
        self.SLEEP = Sleep(self)
        self.RUN = Run(self)
        self.state_machine = StateMachine(
            self.RUN,
            {
                self.SLEEP : {},
                self.IDLE : {},
                self.RUN : {}
            }
        )


    def update(self):
        self.state_machine.update()


    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))


    def draw(self):
        self.state_machine.draw()

    def fire_ball(self):
        ball = Ball(self.x, self.y, self.face_dir * 15)
        game_world.add_object(ball)

