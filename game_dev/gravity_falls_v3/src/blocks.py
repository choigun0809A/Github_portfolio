import pygame as py
import numpy

class Vector:
    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y

class Block:
    def __init__(self, rect: py.rect.FRect = None, color: py.color.Color = None):
        self.collision = True
        self.draw = True
        self.rect = rect if rect else py.rect.FRect(0, 0, 0, 0)
        self.color = color if color else py.color.Color(0, 0, 0)

class Door:
    def __init__(self, rect: py.rect.FRect = None, color: py.color.Color = None, lock: bool = False, l_count: int = 0):
        self.collision = False
        self.draw = True
        self.rect = rect if rect else py.rect.FRect(0, 0, 0, 0)
        self.color = color if color else py.color.Color(0, 0, 0)

        self.Lock = lock
        self.Lock_count = l_count

    def check(self, rect: py.rect.FRect):
        if self.rect.colliderect(rect) and (not self.Lock or self.Lock_count <= 0):
            return True
        return False
    
    def Activate(self):
        
        
        self.Lock_count -= 1
        if self.Lock_count <= 0:
            self.color = py.color.Color(0, 0, 0)
            self.Lock = False

class Player:
    def __init__(self, rect: py.rect.FRect = None, color: py.color.Color = None):
        self.collision = True
        self.draw = True
        self.rect = rect if rect else py.rect.FRect(0, 0, 0, 0)
        self.color = color if color else py.color.Color(0, 0, 0)
        
        self.velocity = Vector(0, 0)
        self.max_vel = 7.5
        self.a = 0.5
        self.decreaser = 0.6
        self.jump = 4

        self.gravity = 0.2

    def Move(self, blocks: list[Block]):
        key = py.key.get_pressed()
        change = Vector()
        if key[py.K_a]:
            change.x -= self.a
        
        if key[py.K_d]:
            change.x += self.a

        
        
        if change.x == 0:
            self.velocity.x *= self.decreaser
        elif numpy.abs(self.velocity.x + change.x) <= self.max_vel:
            self.velocity.x += change.x

        self.velocity.y += self.gravity
        self.rect.y += self.velocity.y

        k = py.key.get_just_pressed()
        for b in blocks:
            
            if self.rect.colliderect(b.rect):
                self.rect.bottom = b.rect.top
                self.velocity.y = 0
                if k[py.K_w] or k[py.K_UP] or k[py.K_SPACE]:
                    self.velocity.y = -self.jump

        self.rect.x += self.velocity.x
        for b in blocks:
            if self.rect.colliderect(b.rect):
                if self.rect.centerx > b.rect.centerx:
                    self.rect.left = b.rect.right+0.2
                else:
                    self.rect.right = b.rect.left-0.2

                self.velocity.x = 0

class Trap_door:
    def __init__(
        self, 
        rect: py.rect.FRect = None, 
        color: py.color.Color = None, 
        code: int = None
        ):
        self.collision = True
        self.draw = True
        self.rect = rect if rect else py.rect.FRect(0, 0, 0, 0)
        self.color = color if color else py.color.Color(0, 0, 0)

        self.code = code if code else 10
    
    def Activate(self):
        self.draw = False
        self.collision = False

class Falling_block:
    def __init__(
        self, 
        rect: py.rect.FRect = None, 
        color: py.color.Color = None, 
        code: int = None, 
        gravity: float = None,
        durration: int = None,
        draw: bool = None,
        collide: bool = False
        ):
        self.collision = collide
        self.draw = draw if draw else False
        self.rect = rect if rect else py.rect.FRect(0, 0, 0, 0)
        self.color = color if color else py.color.Color(0, 0, 0)
        self.gravity = gravity if gravity else float(1)
        self.durration = durration if durration else 0

        self.Active = False
        self.code = code if code else 10
    
    def Activate(self):
        self.Active = True
        self.draw = True
        self.time = py.time.get_ticks()
        
    
    def Move_check(self, player: py.rect.FRect):
        if self.Active:
            self.rect.y += self.gravity
            
            if (py.time.get_ticks() - self.time)> self.durration:
                self.Active = False
                self.draw = False

            if player.colliderect(self.rect):
                return True
            else:
                return False

class Sliding_block:
    def __init__(
        self, 
        rect: py.rect.FRect = None, 
        color: py.color.Color = None, 
        code: int = None, 
        gravity: float = None,
        durration: int = None,
        draw: bool = None,
        collide: bool = False
        ):

        self.collision = collide
        self.draw = draw if draw else False
        self.rect = rect if rect else py.rect.FRect(0, 0, 0, 0)
        self.color = color if color else py.color.Color(0, 0, 0)
        self.gravity = gravity if gravity else float(1)
        self.durration = durration if durration else 0

        self.Active = False
        self.code = code if code else 10
    
    def Activate(self):
        self.Active = True
        self.draw = True
        self.time = py.time.get_ticks()
        
    
    def Move_check(self, player: py.rect.FRect):
        if self.Active:
            self.rect.x += self.gravity
            
            if (py.time.get_ticks() - self.time)> self.durration:
                self.Active = False
                self.draw = False

            if player.colliderect(self.rect):
                return True
            else:
                return False

class Magic_door:
    def __init__(
        self, 
        rect: py.rect.FRect = None, 
        color: py.color.Color = None, 
        code: int = None
        ):
        self.collision = False
        self.draw = False
        self.rect = rect if rect else py.rect.FRect(0, 0, 0, 0)
        self.color = color if color else py.color.Color(0, 0, 0)

        self.code = code if code else 10
    
    def Activate(self):
        if self.draw:
            self.draw = False
            self.collision = False
        else:
            self.draw = True
            self.collision = True
    

class Slide_pushing_block:
    def __init__(
        self, 
        rect: py.rect.FRect = None, 
        color: py.color.Color = None, 
        code: int = None, 
        gravity: float = None,
        durration: int = None,
        draw: bool = None,
        collide: bool = True
        ):

        self.collision = collide
        self.draw = draw if draw else True
        self.rect = rect if rect else py.rect.FRect(0, 0, 0, 0)
        self.color = color if color else py.color.Color(0, 0, 0)
        self.gravity = gravity if gravity else float(1)
        self.durration = durration if durration else 0

        self.Active = False
        self.code = code if code else 10
    
    def Activate(self):
        self.Active = True
        self.draw = True
        self.time = py.time.get_ticks()
        
    
    def Move_check(self, player: py.rect.FRect):
        if self.Active:
            self.rect.x += self.gravity

            
            if (py.time.get_ticks() - self.time)> self.durration:
                self.Active = False
                self.draw = False
                self.collision = False

            if player.colliderect(self.rect):
                player.x += self.gravity


class Slide_y_pushing_block:
    def __init__(
        self, 
        rect: py.rect.FRect = None, 
        color: py.color.Color = None, 
        code: int = None, 
        gravity: float = None,
        durration: int = None,
        draw: bool = None,
        collide: bool = True
        ):

        self.collision = collide
        self.draw = draw if draw else True
        self.rect = rect if rect else py.rect.FRect(0, 0, 0, 0)
        self.color = color if color else py.color.Color(0, 0, 0)
        self.gravity = gravity if gravity else float(1)
        self.durration = durration if durration else 0

        self.Active = False
        self.code = code if code else 10
    
    def Activate(self):
        self.Active = True
        self.draw = True
        self.time = py.time.get_ticks()
        
    
    def Move_check(self, player: py.rect.FRect):
        if self.Active:
            self.rect.y += self.gravity

            
            if (py.time.get_ticks() - self.time)> self.durration:
                self.Active = False
                self.draw = False
                self.collision = False

            if player.colliderect(self.rect):
                player.y += self.gravity



class Door_Trigger:
    def __init__(self, rect: py.rect.FRect = None, color: py.color.Color = None, count: int = None, draw: bool = None):
        self.collision = False
        self.draw = draw if draw else False
        self.rect = rect if rect else py.rect.FRect(0, 0, 0, 0)
        self.color = color if color else py.color.Color(0, 0, 0)
        self.count = count if count else 0

        self.float_speed = 2 * numpy.pi * 2
        self.xo = 1.5



    
    def check(self, rect: py.rect.FRect):
        if self.rect.colliderect(rect):
            return True
        return False

class Trigger:
    def __init__(self, rect: py.rect.FRect = None, color: py.color.Color = None, code: int = None, count: int = None, draw: bool = None):
        self.collision = False
        self.draw = draw if draw else False
        self.rect = rect if rect else py.rect.FRect(0, 0, 0, 0)
        self.color = color if color else py.color.Color(0, 0, 0)
        self.count = count if count else 0

        self.target_code = code if code else 10
    
    def check(self, rect: py.rect.FRect):
        if self.rect.colliderect(rect):
            return True
        return False