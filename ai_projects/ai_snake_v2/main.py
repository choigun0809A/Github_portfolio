import torch, torch.nn as nn, pygame as p, torch.optim as optim, random as rand
import numpy as np, math, sys, copy, pickle
from collections import deque

class Game:
    def __init__(self, size):
        self.size = size
        self.state = [[0 for _ in range(size)] for _ in range(size)]
        self.add_random_fruit()
        self.direction_angle = 90
        self.body: list[p.rect.Rect] = [
            p.rect.Rect(len(self.state[0])//2, len(self.state)//2, 1, 1),
            p.rect.Rect(len(self.state[0])//2, len(self.state)//2+1, 1, 1)
        ]
        self.reward = 0
    
    def reset(self):
        self.state = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.add_random_fruit()
        self.direction_angle = 90
        self.body : list[p.rect.Rect] = [
            p.rect.Rect(len(self.state[0])//2, len(self.state)//2, 1, 1),
            p.rect.Rect(len(self.state[0])//2, len(self.state)//2+1, 1, 1)
        ]
        self.reward = 0
    
    def move(self, action):
        if action == 0:
            direct = p.Vector2(0, -1)
        elif action == 1:
            direct = p.Vector2(0, 1)
        elif action == 2:
            direct = p.Vector2(-1, 0)
        elif action == 3:
            direct = p.Vector2(1, 0)
        
        
        fruit_found = False
        xx, yy = None, None
        for y, row in enumerate(self.state):
            for x, val in enumerate(row):
                if val == 3:
                    xx, yy = x, y
                    fruit_found = True
                    break
            if fruit_found:
                break
        
        if xx == None:
            self.add_random_fruit()
            for y, row in enumerate(self.state):
                for x, val in enumerate(row):
                    if val == 3:
                        xx, yy = x, y
                        fruit_found = True
                        break
                if fruit_found:
                    break
        

        # Compute distance from the snake head to the fruit before moving.
        bhead = self.body[0].copy()
        bx, by = bhead.x, bhead.y
        bdx = xx - bx
        bdy = yy - by
        bdistance = np.sqrt(bdx**2 + bdy**2)

        # Move the head
        head = self.body[0].copy()
        head.x += direct.x
        head.y -= direct.y

        self.body.insert(0, head)

        # Compute new distance after moving
        x, y = head.x, head.y
        dx = xx - x
        dy = yy - y
        distance = np.sqrt(dx**2 + dy**2)
        
        # Check collision with itself
        if any(b.colliderect(head) for b in self.body[1:]):
            self.reward -= 150
            print("bod")
            return True
        else:
            self.reward += 10

        # Check for out-of-bound
        if x < 0 or y < 0 or x >= len(self.state[0]) or y >= len(self.state):
            self.reward -= 150
            print("out")
            return True
        else:
            self.reward += 10
        
        # Handle movement: if the cell doesn't have fruit, remove the tail.
        if self.state[y][x] != 3:
            self.body.pop()
            # self.reward += 40  if distance < bdistance else -10

        # elif self.state[y][x] == 3:
        #     self.state[y][x] = 0
        #     self.reward += 10
        #     print("\nate")
        #     self.add_random_fruit()

        
        return False
    
    def add_random_fruit(self):

        x, y = len(self.state[0]), len(self.state)
        
        x, y = rand.randint(1, x-2), rand.randint(1, y-2)
        self.state[y][x] = 3



class Brain(nn.Module):
    def __init__(self, inputs, outputs):
        super().__init__()
        self.fc = nn.Sequential(
            nn.Linear(inputs, 460),
            nn.ReLU(),
            nn.Linear(460, 460),
            nn.ReLU(),
            nn.Linear(460, 320),
            nn.ReLU(),
            nn.Linear(320, 260),
            nn.ReLU(),
            nn.Linear(260, 100),
            nn.ReLU(),
            nn.Linear(100, 50),
            nn.ReLU(),
            nn.Linear(50, outputs)
        )
        self.memories = deque(maxlen= 10000)
        self.remember_size = 1500

        self.loss_fc = nn.SmoothL1Loss()
        self.optimizer = optim.Adam(self.parameters(), lr = 0.001)
    
    def memorize(self, action, reward, state, next_state, done):
        self.memories.append((action, reward, state, next_state, done))
    
    def remember_at_random(self):
        if len(self.memories) >= self.remember_size:
            memory = rand.sample(self.memories, self.remember_size)
            actions, rewards, states, next_states, dones = zip(*memory)

            states = torch.cat(states).float()     
            next_states = torch.cat(next_states).float()  
            actions = torch.LongTensor(actions)  
            rewards = torch.FloatTensor(rewards)  
            dones = torch.FloatTensor(dones)


            preds = self(states)
            

            targets = preds.clone().detach()

            next_preds = self(next_states)
            max_next_qs = torch.max(next_preds, dim = 1)[0]

            target_q_values = rewards + 0.99 * max_next_qs * (1 - dones)
            
            
            for i in range(len(actions)):
                targets[i, actions[i]] = target_q_values[i]



            self.optimizer.zero_grad()
            loss = self.loss_fc(preds, targets)
            loss.backward()
            self.optimizer.step()
        
    def norm_train(self, state, action, reward):

        pred = self(state)
        target = pred.clone().detach()
        target[0, action] = reward

        self.optimizer.zero_grad()
        loss = self.loss_fc(pred, target)
        loss.backward()
        self.optimizer.step()
    

    def forward(self, x):
        return self.fc(x)


inputs = 20*20
brain = Brain(inputs, 4)
try:
    brain.load_state_dict(torch.load("brain.pth"))
    with open("mem.pkl", "rb") as f:
        loaded_mem = pickle.load(f)
        brain.memories = deque(loaded_mem, maxlen=10000)
except:
    pass

snake_game = Game(20)



screen = p.display.set_mode((800, 800))

block_size = 800 / 20
epsilon = 0.5
while True:
    done = False
    clock = p.time.Clock()
    fps = 60
    snake_game.reset()
    if len(brain.memories) > brain.remember_size:
        brain.remember_at_random()
    while not done:
        # draw
        screen.fill("BLACK")
        for y, row in enumerate(snake_game.state):
            for x, val in enumerate(row):
                if val == 3:
                    p.draw.rect(
                        screen,
                        "RED" ,
                        p.rect.FRect(
                            x * block_size, y*block_size,
                            block_size, block_size
                        )
                    )
        for pos, bod in enumerate(snake_game.body):
            
            p.draw.rect(
                screen,
                "GREEN",
                p.rect.FRect(
                    bod.x * block_size, bod.y*block_size,
                    block_size, block_size
                )
            )
        
        if len(brain.memories) > brain.remember_size:
            
            epsilon = 0.1
            state = copy.deepcopy(snake_game.state)

            for pos, bod in enumerate(snake_game.body):
                state[bod.y][bod.x] = 1 if pos == 0 else 2
            flattaned_state = torch.tensor(state, dtype=torch.float32).flatten().unsqueeze(0)
            
            pred = brain(flattaned_state)
            # 10% of the time, pick a random action
            if rand.random() < epsilon:
                action = rand.randint(0, 3)  # Assuming 3 possible actions: left, straight, right
                epsilon *= 0.998
            else:
                action = torch.argmax(pred).item()
                
            
            done = snake_game.move(action)
            after_state = copy.deepcopy(snake_game.state)

            for pos, bod in enumerate(snake_game.body):
                try:
                    after_state[bod.y][bod.x] = 1 if pos == 0 else 2
                except:
                    pass
            
            brain.memorize(action, snake_game.reward, flattaned_state, torch.tensor(after_state, dtype=torch.float32).flatten().unsqueeze(0), done)
            
            snake_game.reward = 0
        else:
            state = copy.deepcopy(snake_game.state)

            for pos, bod in enumerate(snake_game.body):
                state[bod.y][bod.x] = 1 if pos == 0 else 2
            flattaned_state = torch.tensor(state, dtype=torch.float32).flatten().unsqueeze(0)
            
            pred = brain(flattaned_state)
            # 10% of the time, pick a random action
            if rand.random() < epsilon:
                action = rand.randint(0, 3)  # Assuming 3 possible actions: left, straight, right
                epsilon *= 0.998
            else:
                action = torch.argmax(pred).item()
                
            
            done = snake_game.move(action)
            # print(action, snake_game.reward, epsilon)

            brain.norm_train(flattaned_state, action, snake_game.reward)

            after_state = copy.deepcopy(snake_game.state)

            for pos, bod in enumerate(snake_game.body):
                try:
                    after_state[bod.y][bod.x] = 1 if pos == 0 else 2
                except:
                    pass
            
            brain.memorize(action, snake_game.reward, flattaned_state, torch.tensor(after_state, dtype=torch.float32).flatten().unsqueeze(0), done)
            
            snake_game.reward = 0

        p.display.update()
        clock.tick(5)
        for e in p.event.get():
            if e.type == p.QUIT:
                torch.save(brain.state_dict(), "brain.pth")
                with open("mem.pkl", "wb") as f:
                    pickle.dump(list(brain.memories), f)
                print(f"saved memories: {len(list(brain.memories))})")
                # print()
                # for pos, bod in enumerate(snake_game.body):
                #     print(bod.x, bod.y, len(snake_game.body))
                # for row in state:
                #     for val in row:
                #         print(val, end="")
                #     print()
                # print()
                
                # for row in after_state:
                #     for val in row:
                #         print(val, end="")
                #     print()
                p.quit()
                sys.exit()


