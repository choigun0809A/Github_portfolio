import pygame as pg, random as rand, copy, numpy as np


state = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
]
direct = pg.Vector2(0, -1)

body: list[pg.rect.Rect] = [
    pg.rect.Rect(len(state[0])//2, len(state)//2, 1, 1),
    pg.rect.Rect(len(state[0])//2, len(state)//2+1, 1, 1)
]

def reset():
    global state, body, direct
    direct = pg.Vector2(0, -1)
    

    body = [
        pg.rect.Rect(len(state[0])//2, len(state)//2, 1, 1),
        pg.rect.Rect(len(state[0])//2, len(state)//2+1, 1, 1)
    ]
    state = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
    ]
    add_random_fruit()

def add_random_fruit():
    global state
    x, y = len(state[0]), len(state)
    
    x, y = rand.randint(1, x-2), rand.randint(1, y-2)
    state[y][x] = 3

add_random_fruit()
reward = 0

def move(dir: str):
    global direct, body, state, reward
    if dir == "up":
        direct = pg.Vector2(0, -1)
    elif dir == "down":
        direct = pg.Vector2(0, 1)
    elif dir == "left":
        direct = pg.Vector2(-1, 0)
    elif dir == "right":
        direct = pg.Vector2(1, 0)
    
    # Find the fruit's coordinates, and break out of both loops when found.
    fruit_found = False
    xx, yy = None, None
    for y, row in enumerate(state):
        for x, val in enumerate(row):
            if val == 3:
                xx, yy = x, y
                fruit_found = True
                break
        if fruit_found:
            break
    if xx == None:
        add_random_fruit()
        for y, row in enumerate(state):
            for x, val in enumerate(row):
                if val == 3:
                    xx, yy = x, y
                    fruit_found = True
                    break
            if fruit_found:
                break
    

    # Compute distance from the snake head to the fruit before moving.
    bhead = body[0].copy()
    bx, by = bhead.x, bhead.y
    bdx = xx - bx
    bdy = yy - by
    bdistance = np.sqrt(bdx**2 + bdy**2)

    # Move the head
    head = body[0].copy()
    head.centerx += direct.x
    head.centery += direct.y
    body.insert(0, head)

    # Compute new distance after moving
    x, y = head.x, head.y
    dx = xx - x
    dy = yy - y
    distance = np.sqrt(dx**2 + dy**2)
    
    # Check collision with itself
    for pos, bod in enumerate(body):
        if pos != 0 and bod.colliderect(head):
            reward -= 50
            return True

    # Check for out-of-bound
    if x < 0 or y < 0 or x >= len(state[0]) or y >= len(state):
        reward -= 200
        return True

    # Handle movement: if the cell doesn't have fruit, remove the tail.
    if state[y][x] != 3:
        body.pop()
        reward += 40 * len(body) if distance < bdistance else -15 * len(body) / 2

    elif state[y][x] == 3:
        state[y][x] = 0
        reward += 100 * len(body)
        print("\nate")
        add_random_fruit()
    
    return False

    


    


    