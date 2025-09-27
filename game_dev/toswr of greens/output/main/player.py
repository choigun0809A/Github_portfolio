import pygame, random as rand
import numpy as np

class Player:
    def __init__(self):
        self.frame_speed_in_int = 200
        self.state = "idle"
        self.row = {
            "idle": 0,
            "walk": 1,
            "attack1": 2,
            "attack2": 3,
            "attack3": 4,
            "hit": 5,
            "die": 6,
        }
        self.frames = {
            "idle": 4,
            "walk": 8,
            "attack1": 6,
            "attack2": 4,
            "attack3": 8,
            "hit": 2,
            "die": 3,
        }
        self.img_size = 100
        self.drawing_size = 200
        self.pos = pygame.Vector2(0, 0)
        
        
        self.Animations = {
            "right": pygame.image.load("imgs/player/axe_men.png").convert(),
        }

        self.bonus_anime = False
        self.bonus_anime_name = ""
        self.bonus_anime_start = 0
        self.bonus_anime_speed = 100

        self.velocity = pygame.Vector2(0, 0)
        self.speed = 1
        self.deceleration = 0.5
        self.max_speed = 4

    def Move(self):
        keys = pygame.key.get_pressed()
        change = pygame.Vector2(0, 0)
        
        if keys[pygame.K_w]:
            change.y -= self.speed
        if keys[pygame.K_s]:
            change.y += self.speed
        if keys[pygame.K_a]:
            change.x -= self.speed
        if keys[pygame.K_d]:
            change.x += self.speed

        self.state = "walk" if change.x + change.y != 0 else "idle"

        self.velocity += change
        if abs(self.velocity.x) > self.max_speed:
            self.velocity.x -= change.x
        if abs(self.velocity.y) > self.max_speed:
            self.velocity.y -= change.y
        
        if change.x == 0:
            self.velocity.x *= self.deceleration
        if change.y == 0:
            self.velocity.y *= self.deceleration
        
        self.pos += self.velocity

        if keys[pygame.K_f] and not self.bonus_anime:
            self.bonus_anime = True
            self.bonus_anime_name = f"attack{rand.randint(1, 3)}"
            self.bonus_anime_start = pygame.time.get_ticks()


    def Draw(self, screen: pygame.Surface):
        if not self.bonus_anime:
            
            frame = (pygame.time.get_ticks() % (self.frames[self.state] * self.frame_speed_in_int)) // self.frame_speed_in_int
            sprite_sheet = self.Animations["right"]

            frame_rect = pygame.Rect(
                frame * self.img_size,
                self.row[self.state] * self.img_size,
                self.img_size,
                self.img_size
            )
        
        else:
            frame = ((pygame.time.get_ticks() - self.bonus_anime_start) % (self.frames[self.bonus_anime_name] * self.bonus_anime_speed)) // self.bonus_anime_speed
            sprite_sheet = self.Animations["right"]


            frame_rect = pygame.Rect(
                frame * self.img_size,
                self.row[self.bonus_anime_name] * self.img_size,
                self.img_size,
                self.img_size
            )

            if self.frames[self.bonus_anime_name] == frame + 1:
                self.bonus_anime = False
            print(self.frames[self.bonus_anime_name])
        
        sprite = sprite_sheet.subsurface(frame_rect)
        sprite = pygame.transform.flip(sprite, True, False) if self.velocity.x < 0 else sprite
        sprite = pygame.transform.scale(sprite, (self.drawing_size, self.drawing_size))
        screen.blit(sprite, self.pos)
        