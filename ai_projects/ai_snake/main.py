import pygame as pg, MAP, torch, torch.nn as nn, torch.optim as optim, sys
import copy

class agent(nn.Module):
    def __init__(self, input_amount, output_amount):
        super().__init__()
        self.fc = nn.Sequential(
            nn.Linear(input_amount, 250),
            nn.ReLU(),
            nn.Linear(250, 200),
            nn.ReLU(),
            nn.Linear(200, 120),
            nn.ReLU(),
            nn.Linear(120, 100),
            nn.ReLU(),
            nn.Linear(100, output_amount)
        )
    
    def forward(self, x):
        return self.fc(x)


snake_master = agent(15 * 15, 4)
try:
    snake_master.load_state_dict(torch.load("snake_mem.pth"))
except:
    pass
optimizer = optim.Adam(snake_master.parameters(), lr = 0.001)
lose_fc = nn.SmoothL1Loss()

screen = pg.display.set_mode((800, 800))
pixel_size = screen.width/len(MAP.state)
clock = pg.time.Clock()
start = 0
speed = 10

from collections import deque
memory = deque(maxlen= 10000)

for _ in range(9999999999999999999999999999999):

    done = False
    while not done:
        if (pg.time.get_ticks() - start)//speed >= 1:
            start = pg.time.get_ticks()


            ## adding body
            map_copy = copy.copy(MAP.state)
            for pos, rec in enumerate(MAP.body):
                adder = 2
                if pos == 0:
                    adder = 1
                map_copy[rec.y][rec.x] = adder

            ## made a digestible input
            processed_state = torch.FloatTensor(map_copy).flatten().unsqueeze(0)
            

            probs = snake_master(processed_state)
            action = torch.argmax(probs).item()

            d = "up"
            if action == 1:
                d = "down"
            elif action == 2:
                d = "left"
            elif action == 3:
                d = "right"
            done = MAP.move(d)
            target = probs.clone().detach()
            target[0, action] = MAP.reward
            loss = lose_fc(probs, target) 
            MAP.reward = 0
    
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        
        screen.fill("BLACK")
        if pg.key.get_just_pressed()[pg.K_q] and speed > 10:
            speed -= 10
            print(speed)
        elif pg.key.get_just_pressed()[pg.K_e]:
            speed += 10
            print(speed)

        for y, row in enumerate(MAP.state):
            for x, val in enumerate(row):
                if val == 3:
                    pg.draw.rect(
                        screen,
                        "GREEN",
                        pg.rect.Rect(x * pixel_size, y * pixel_size, pixel_size, pixel_size)
                    )
        
        for rec in MAP.body:
            pg.draw.rect(
                screen,
                "RED",
                pg.rect.Rect(rec.x * pixel_size, rec.y * pixel_size, pixel_size, pixel_size)
            )


        pg.display.flip()
        clock.tick(0)
        for e in pg.event.get():
            if e.type == pg.QUIT:
                torch.save(snake_master.state_dict(), "snake_mem.pth")
                pg.quit()
                sys.exit()
    MAP.reset()

