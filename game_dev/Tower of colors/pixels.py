import pyray as rl
import raylib as rll
import numpy as np
import random as rand

class Player:
    def __init__(self, size: rl.Vector2, color: rl.Color):
        self.rect = rl.Rectangle(
            (rl.get_screen_width()/2 - size.x/2),
            (rl.get_screen_height()/2 - size.y/2),
            size.x, 
            size.y,
            )
        self.color = color

        self.velocity = rl.Vector2(0, 0)
        self.max_speed = 5
        self.speed = 1
        self.deceleration = 0.5

    def move(self):
        
        change = rl.Vector2(0, 0)
        if rl.is_key_down(rll.KEY_W):
            change.y -= self.speed
        if rl.is_key_down(rll.KEY_S):
            change.y += self.speed
        if rl.is_key_down(rll.KEY_A):
            change.x -= self.speed
        if rl.is_key_down(rll.KEY_D):
            change.x += self.speed
        
        self.velocity.y += change.y
        self.velocity.x += change.x
        if np.abs(self.velocity.x) > self.max_speed:
            self.velocity.x -= change.x
        if np.abs(self.velocity.y) > self.max_speed:
            self.velocity.y -= change.y

        if change.x == 0:
            self.velocity.x *= self.deceleration
        if change.y == 0:
            self.velocity.y *= self.deceleration
        
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
    
    def draw(self):
        rl.draw_rectangle_rounded(
            self.rect,
            0.2,
            120,
            self.color
        )
        # rl.draw_rectangle_pro(
        #     self.rect,
        #     rl.Vector2(0, 0),
        #     0,
        #     self.color
        # )



class Follower:
    def __init__(self, size: rl.Vector2, color: rl.Color):
        self.rect = rl.Rectangle(
            (rl.get_screen_width()/2 - size.x/2),
            (rl.get_screen_height()/2 - size.y/2),
            size.x, 
            size.y,
        )
        self.color = color
        self.want = False
        self.cooldown = 1000
        self.start = rl.get_time()
        self.refreshed = False
        self.velocity = rl.Vector2(0, 0)
        self.speed = 1 
        self.max_speed = 4
    
    def behave(self, player: rl.Rectangle):
        if self.want:
            self.move(player)
        
        if not self.refreshed:
            self.want = rand.choice((True, False, True))
            self.refreshed = True
            self.start = rl.get_time()
        else:
            if 1000*(rl.get_time() - self.start) > self.cooldown:
                self.refreshed = False

    
    def move(self, player_rect: rl.Rectangle):
        x, y = player_rect.x + player_rect.width/2, player_rect.y + player_rect.height/2
        xx, yy = self.rect.x + self.rect.width/2, self.rect.y + self.rect.height/2
        
        dx = x - xx
        dy = y - yy

        
        if dx != 0:
            px = int(dx // np.abs(dx))
        else:
            px = 0 

        if dy != 0:
            py = int(dy // np.abs(dy))
        else:
            py = 0 
        
        self.velocity.x += self.speed * px
        self.velocity.y += self.speed * py

        if np.abs(self.velocity.x) > self.max_speed:
            self.velocity.x -= self.speed * px
        if np.abs(self.velocity.y) > self.max_speed:
            self.velocity.y -= self.speed * py
        
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        

    def draw(self):
        rl.draw_rectangle_rounded(
            self.rect,
            0.2,
            120,
            self.color
        )