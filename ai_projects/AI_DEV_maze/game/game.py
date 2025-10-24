import random as rand
import torch
import copy

gamma = torch.tensor(0.9, dtype=torch.float)
alpha = torch.tensor(0.5, dtype=torch.float)
random_chance = 0.2

batch = []
batch_max_size = 900
batch_size = 32

tick = 0.05
t_tick = tick
saved_time = 0
time_limit = 5


min_penalty = 2
reward_decrease_per_tick = min_penalty / (time_limit/tick)
r = 0

trial = 0

class Object:
    __slots__ = ["x", "y"]
    def __init__(self, x, y):
        self.x = x
        self.y = y



items = []
blocks = []


terrain_index = 0
terrain = []

saved_maps = [
    [
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,1,0,0,0,0,0],
        [0,0,0,0,2,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,2,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,2,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0]
    ],
    [
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,2,0,0,0,0,0,0,0],
        [0,0,0,0,1,0,0,0,0,0],
        [0,0,0,0,2,0,0,0,2,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,2,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0]
    ],
    [
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,1,0,0,0,2,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,2,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,2,0,0,0,2,0],
        [0,0,0,0,0,0,0,0,0,0]
    ],
    [
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,1,0,0,0,2,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,2,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,3,0,0],
        [0,0,0,0,0,0,3,3,0,0],
        [0,0,0,0,2,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0]
    ],
    [
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,1,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,3,0,0],
        [0,0,0,0,0,0,0,3,2,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,3,3,3,0,0,0,0],
        [0,0,0,0,2,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0]
    ],
    [
        [0,0,0,0,0,0,0,0,0,0],
        [0,2,3,0,0,0,0,3,0,0],
        [0,3,3,0,1,0,0,3,0,0],
        [0,0,0,0,0,0,0,3,2,0],
        [0,0,0,0,0,0,0,3,0,0],
        [0,3,2,0,0,0,0,0,0,0],
        [0,3,3,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,2,3,0,0,0,0],
        [0,0,0,0,0,3,0,0,0,0]
    ],
    [
        [0,0,0,0,0,0,0,0,0,0],
        [2,3,0,0,0,0,0,3,0,0],
        [0,3,0,0,1,0,0,3,0,0],
        [0,3,0,0,0,0,0,3,2,0],
        [0,0,0,0,0,0,0,3,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,3,3,3,3,0,3,3,3,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,2,0,0,0,0,0,2,0]
    ]
]


player = Object(0,0)
two_steps_back = Object(0,0)
discovered_positions = []

step = 0
step_set = False
origin_position = Object(0,0)
onetime_set = True

def register_terrain():
    global terrain, onetime_set, items, blocks, player
    for y, row in enumerate(terrain):
        for x, val in enumerate(row):
            
            if val == 2:
                if [x, y] not in items:
                    items.append([x, y])
            
            if val == 3:
                if [x, y] not in items:
                    blocks.append([x, y])
                
            elif val == 1:
                player.x = x
                player.y = y
                terrain[y][x] = 0
                
                origin_position.x = x
                origin_position.y = y
            
def show_terrain(pos: int = None):
    global onetime_set, player, origin_position
    if pos is not None:
        for y, row in enumerate(saved_maps[pos]):
            for x, val in enumerate(row):
                
                if val == 2:
                    print("O", end=" ")
                    
                elif val == 0:
                    if x == player.x and y == player.y:
                        print("X", end=" ")
                    else:
                        print(".", end=" ")
                elif val == 3:
                    print("#", end=" ")
                
                    
            print()
    for y, row in enumerate(terrain):
        for x, val in enumerate(row):
            
            if val == 2:
                print("O", end=" ")
                
            elif val == 0:
                if x == player.x and y == player.y:
                    print("X", end=" ")
                else:
                    print(".", end=" ")
            elif val == 3:
                print("#", end=" ")
            
                
        print()
        
def prepare_terrain():
    global terrain
    copyy = copy.deepcopy(terrain)
    copyy[player.y][player.x] = 1
    
    
    players = [[0 for _ in range(len(copyy[0]))] for _ in range(len(copyy))]
    players[player.y][player.x] = 1
    coins = [[0 for _ in range(len(copyy[0]))] for _ in range(len(copyy))]
    for item in items:
        coins[item[1]][item[0]] = 1
    blocks_ = [[0 for _ in range(len(copyy[0]))] for _ in range(len(copyy))]
    for block in blocks:
         blocks_[block[1]][block[0]] = 1
    
    return torch.tensor([[players, coins, blocks_]], dtype=torch.float)
    
    return torch.tensor([copyy], dtype=torch.float).flatten(1, 2)
     
def is_position_goal():
    val = terrain[player.y][player.x]
    if val == 2:
        return True
    else:
        return False

def is_position_wall():
    val = terrain[player.y][player.x]
    if val == 3:
        return True
    else:
        return False
    
def update(action: int)-> bool:
    global player
    
    if action == 0:
        player.y -= 1
    elif action == 1:
        player.y += 1
    elif action == 2:
        player.x -= 1
    elif action == 3:
        player.x += 1
    
    if player.x < 0 or player.x >= len(terrain[0]) or player.y < 0 or player.y >= len(terrain):
        return False
    return True

def reverse_action(action: int):
    if action == 0:
        return 1
    elif action == 1:
        return 0
    elif action == 2:
        return 3
    elif action == 3:
        return 2

def min_distance():
    maxx = int(1e9)
    for item in items:
        distance = (abs(item[0] - player.x)**2 + abs(item[1] - player.y)**2)**0.5
        maxx = min(maxx, distance)
    
    return maxx

def reset_terrain():
    global terrain, player, origin_position
    terrain = copy.deepcopy(saved_maps[terrain_index])
    register_terrain()
    
    player.x = origin_position.x
    player.y = origin_position.y

def next_step():
    global terrain_index
    if len(items) == 0:
        terrain_index += 1
        if terrain_index >= len(saved_maps):
            terrain_index = 0
        
        reset_terrain()