import pygame as py
import perlin_noise

class Vector:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y



class Game:
    def __init__(self, screen_size:Vector , screen_name:str):
        self.screen = py.display.set_mode((screen_size.x, screen_size.y), py.RESIZABLE)
        py.display.set_caption(screen_name)
        
        self.gravity = 2
        self.player: Body = Body()
        self.enemies: list[Body] = []

class Sprite:
    def __init__(self):
        self.imgs = {}
        self.speeds = {}
        self.collideables = {}

class Body:
    def __init__(self):
        self.sprite: Sprite = Sprite()
        self.pos:Vector = Vector()
        self.velocity:Vector = Vector()
        self.type: str = ""
        self.state: str = ""
        self.speed = 0
        self.max_speed = 0
        self.size = 0
        self.facing_left: bool = False

