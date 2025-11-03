from pico2d import *
import game_world
import game_framework

PIXEL_PER_METER = (1.0 / 0.03)
GRAVITY = 9.8

class Ball:
    image = None

    def __init__(self, x = 400, y = 300, throwin_speed = 15, throwin_angle = 45):
        if Ball.image == None:
            Ball.image = load_image('ball21x21.png')
        self.x, self.y = x, y
        self.xv = throwin_speed * math.cos(math.radians(throwin_angle))
        self.yv = abs(throwin_speed * math.sin(math.radians(throwin_angle)))

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        # y축 속도에 중력 가속도 적용
        self.yv -= GRAVITY * game_framework.frame_time # m/s

        # 위치 업데이트
        self.x += self.xv * game_framework.frame_time * PIXEL_PER_METER
        self.y += self.yv * game_framework.frame_time * PIXEL_PER_METER

        # 지면 충돌 처리
        if self.y < 60:
            game_world.remove_object(self)

        if self.x < 0 or self.x > 1600:
            game_world.remove_object(self)
