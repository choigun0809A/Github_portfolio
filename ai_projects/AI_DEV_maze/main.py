from model import model_v1
from game import game as g
import os

import time 

def save_model():
    g.torch.save(model.state_dict(), "models/model.pt")


model = model_v1.ModelV4(output_size=4)



def action_():
    state = g.prepare_terrain()
    output: g.torch.Tensor = model(state)
    
    action = output[0].argmax(0).item()
    
    if g.rand.randint(0, 100) < g.random_chance * 100:
        action = g.rand.randint(0, 3)
    
    return state, action


def train():
    state, action, reward, next_state = zip(*g.rand.sample(g.batch, g.batch_size))
    state = g.torch.cat(state)
    action = g.torch.cat(action)
    reward = g.torch.cat(reward)
    next_state = g.torch.cat(next_state)
    
    output: g.torch.Tensor = model(state)
    target = output.clone()
    
    output2 = model(next_state)
    maxs = output2.max(1)[0]
    r = reward + g.gamma * maxs
    target[range(g.batch_size), action] = target[range(g.batch_size), action] + g.alpha* (r - output[range(g.batch_size), action])
    
    model.optimizer.zero_grad()
    loss = model.mse(output, target)
    loss.backward()
    model.optimizer.step()

def session():
    reward = 0
    
    state, action = action_()
    reversed_action = False
    
    
    # before_distance = g.min_distance()
    
    # print(g.player.x, g.player.y, len(g.terrain), len(g.terrain), g.terrain)
    
    ## -- update -- ##
    if not g.update(action):
        reward = -4
        reversed_action = True
        g.update(g.reverse_action(action))
    
    if g.step == 0:
        g.two_steps_back.x = g.player.x
        g.two_steps_back.y = g.player.y
    
    if [g.player.x, g.player.y] not in g.discovered_positions:
        reward += 2
        g.discovered_positions.append([g.player.x, g.player.y])
        
        
    g.step += 1
    if g.step >= 2:
        if g.two_steps_back.x == g.player.x and g.two_steps_back.y == g.player.y:
            reward = -4
            g.step_set = False
    
    # after_distance = g.min_distance()
    
    if reversed_action:
        pass
        
    else:
        # # ## -- get close -- ##
        # if before_distance > after_distance:
        #     reward += 1
        
        hit_wall = False
        ## -- check if the position is a wall -- ##
        if g.is_position_wall():
            reward += -4
            hit_wall = True
            
        elif g.is_position_goal():
            reward += 5 + g.r
            g.terrain[g.player.y][g.player.x] = 0
            for item in g.items:
                if item[0] == g.player.x and item[1] == g.player.y:
                    g.items.remove(item)
                    break
            g.next_step()
        
        if hit_wall:
            g.update(g.reverse_action(action))
    
    
        
        
    next_state = g.prepare_terrain()
    g.batch.append(
        (
            state,
            g.torch.tensor([action]),
            g.torch.tensor([reward], dtype=g.torch.float),
            next_state
        )
    )
    if len(g.batch) > g.batch_max_size:
        g.batch.pop(0)

def loop():
    
    g.saved_time += g.tick
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("Time limit:", g.time_limit)
    print("Time:", int(g.saved_time))
    print(f"Stage: {g.terrain_index + 1}")
    print(f"Trial: {g.trial + 1}")
    
    ## -- draw --##
    g.show_terrain()
    
    session()
    
    g.r += -g.reward_decrease_per_tick
    
    
    if g.saved_time >= g.time_limit:
        g.saved_time = 0
        g.trial += 1
        g.r = 0
        if len(g.batch) > g.batch_size:
            for _ in range(3):
                train()
        
        
        g.reset_terrain()
        
    time.sleep(g.t_tick)

if __name__ == "__main__":
    g.saved_time = 0
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Levels:")
    for level in range(len(g.saved_maps)):
        g.show_terrain(level)
        print("\n\n#######################\n\n")
    
    input("Press enter to start")
    
    g.reset_terrain()
    
    while True:
        loop()
    
