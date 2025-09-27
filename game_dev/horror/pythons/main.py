import pygame as py
import sys, numpy
from extras.common_tools import *


game = None


# def gravity():
#     game.player.velocity.y += game.gravity

def player_draw():
    global game

    img = game.player.sprite.imgs[game.player.state]
    time = game.player.sprite.speeds[game.player.state]
    scale = game.player.size / img.height

    amount = img.width / img.height
    frame = py.time.get_ticks() % (amount * time) // time

    cutted = py.Surface((img.height, img.height))
    cutted.blit(img, (0, 0), py.Rect(frame *img.height, 0, img.height, img.height))
    cutted = py.transform.scale_by(cutted, scale)

    if game.player.facing_left:
        cutted = py.transform.flip(cutted, True, False)

    game.screen.blit(cutted, game.player.pos)

def player_rule():
    speed = game.player.speed
    key = py.key.get_pressed()

    moved = False

    
    if key[py.K_w]and numpy.abs(game.player.velocity.y - speed) <= game.player.max_speed:
        moved= True
        game.player.velocity.y -= speed
    elif key[py.K_s]and numpy.abs(game.player.velocity.y + speed) <= game.player.max_speed:
        moved= True
        game.player.velocity.y += speed
    elif not key[py.K_w] and not key[py.K_s]:
        if game.player.velocity.y > 0:
            game.player.velocity.y -= 1
        elif game.player.velocity.y < 0:
            game.player.velocity.y += 1
    else:
        moved = True

    if key[py.K_a] and numpy.abs(game.player.velocity.x - speed) <= game.player.max_speed:
        moved= True
        game.player.velocity.x -= speed
        game.player.facing_left = True
    elif key[py.K_d] and numpy.abs(game.player.velocity.x + speed) <= game.player.max_speed:
        moved= True
        game.player.velocity.x += speed
        game.player.facing_left = False
    elif not key[py.K_d] and not key[py.K_a]:
        if game.player.velocity.x > 0:
            game.player.velocity.x -= 1
        elif game.player.velocity.x < 0:
            game.player.velocity.x += 1
    else:
        moved = True

    if moved:
        game.player.state = "run"
    else:
        game.player.state = "idle"


    game.player.pos.x += game.player.velocity.x
    game.player.pos.y += game.player.velocity.y





def main():
    global game


    clock = py.time.Clock()
    while True:
        for e in py.event.get():
            if e.type == py.QUIT:
                py.quit()
                sys.exit()

        game.screen.fill("black")
        player_draw()
        player_rule()
        # gravity()


        py.display.flip()
        clock.tick(60)

def load():
    global game
    game = Game(
        Vector(900, 900),
        "name"
    )
    load_player()
  
def load_player():
    global game
    player = Body()
    size = 100
    player.speed = 1
    player.max_speed = 10
    player.type = "player"
    player.state = "idle"
   

    player.sprite.imgs = {
        "idle": py.image.load("imgs/idle.png").convert_alpha(),
        "run": py.image.load("imgs/run.png").convert_alpha(),
        "die": py.image.load("imgs/die.png").convert_alpha(),
        }
    player.sprite.speeds = {
        "idle": 150,
        "run": 110,
        "die": 150,
    }
    
    player.sprite.collideables = {
        "idle": 0.9,
        "run": 0.9,
        "die": 0.9,
    }
    player.size = size
    player.pos = py.rect.FRect(100, 100, size, size)


    game.player = player

    

load()
main()


