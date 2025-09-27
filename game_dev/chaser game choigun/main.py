
import sys
import pygame
import random as rand

def count_down():
  global cooldown, font, global_time, font
  cooldown1 = 0
  if cooldown == 10:
    start_time = pygame.time.get_ticks()
    check_time = (start_time-global_time)//1000
    if check_time < cooldown:
      cooldown1 = cooldown-check_time
    if check_time == cooldown:
      cooldown=0  
    cooldown_text = font.render("cooldown: " +str(cooldown1), True, "black")
    screen.blit(cooldown_text, (0, 14))
  else:
    cooldown_text = font.render("POWER READY", True, "black")
    screen.blit(cooldown_text, (0, 14))

pygame.init()

#screen
screen = pygame.display.set_mode((600,400))
pygame.display.set_caption("chaser")
#start
start_box = pygame.Rect(250,50,100,50)
font = pygame.font.Font(None, 24)
start_text = font.render("Start", True, "black")
start_text1 = start_text.get_rect(center = start_box.center)
show_menu = True
clock = pygame.time.Clock()
#click char
char_coords = pygame.Rect(250,110,100,50)
char_text = font.render("colour", True, "black")
text_coords1 = char_text.get_rect(center = char_coords.center)
#player
x, y = 275, 350
speed = 2
#coin
x1, y1 = rand.randint(0, 570), rand.randint(0, 370)
#point
point = 0
font = pygame.font.Font(None, 24)
coin = font.render("coin: " +str(point), True, "black")
#esc
esc = pygame.Rect((560, 0, 40, 40))
#power space cooldown
cooldown = 0
#enemy info
x2, y2 = 290, 0
show_score = False
point1 = 0
#player colour
player_colour = "grey"

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
    if event.type == pygame.MOUSEBUTTONDOWN:
      if start_box.collidepoint(event.pos):
        
        #player
        x, y = 275, 350
        speed = 2
        #coin
        x1, y1 = rand.randint(0, 570), rand.randint(0, 370)
        #point
        point = 0
        cooldown = 0
        #enemy info
        x2, y2 = 290, 0
        show_menu = False
    if event.type == pygame.MOUSEBUTTONDOWN:
      if esc.collidepoint(event.pos):
        #player
        x, y = 275, 350
        #coin coords in x y
        x1, y1 = rand.randint(0, 570), rand.randint(0, 370)
        #point
        point = 0
        coin = font.render("coin: " +str(point), True, "black")
        show_menu = True
        show_score = False
    #colour
    if event.type == pygame.MOUSEBUTTONDOWN:
      if char_coords.collidepoint(event.pos):
        if player_colour == "grey":
          player_colour = "red"
        elif player_colour == "red":
          player_colour = "blue"   
        elif player_colour == "blue":
          player_colour = "green"
        elif player_colour == "green":
          player_colour = "grey"

  screen.fill("white")
  if show_menu:
    #enemy info
    x2, y2 = 290, 0
    pygame.draw.rect(screen, "grey", start_box)
    pygame.draw.rect(screen, "green" if start_box.collidepoint(pygame.mouse.get_pos()) else "grey", start_box)
    screen.blit(start_text, start_text1)
    pygame.draw.rect(screen, f"{player_colour}", char_coords)
    screen.blit(char_text, text_coords1)
    if show_score:
      font2 = pygame.font.Font(None, 34)
      score_show = font2.render("score: " +str(point1), True, "black")
      screen.blit(score_show, (255, 0))
  else:
    #enemy info
    if x2+7 < x+25:
      x2+=1
    else:
      x2-=1
    if y2+7 > y+25:
      y2-=1
    else:
      y2+=1
    if x2+15 > x and x2 < x+50 and y2+15 > y and y2 < y+50:
      speed=0
      point1 = point
      show_score = True
      show_menu = True
    pygame.draw.rect(screen, "red", (x2, y2, 15, 15))
    #player info
    key = pygame.key.get_pressed()
    if key[pygame.K_w] and y-1>0:
      y-=speed
    if key[pygame.K_a] and x-1>0:
      x-=speed
    if key[pygame.K_s] and y+50+1<400:
      y+=speed
    if key[pygame.K_d] and x+50+1<600:
      x+=speed
    if key[pygame.K_SPACE] and cooldown==0:
      x=rand.randint(0, 570)
      y=rand.randint(0, 370)
      x2=rand.randint(0, 585)
      y2=rand.randint(0, 385)
      cooldown = 10
      global_time = pygame.time.get_ticks()
      
    count_down()
    screen.blit(coin, (0,0))
    if x1+15>x and y1+15>y and y+50>y1+15 and x+50>x1+15:
      x1, y1 = rand.randint(0, 570), rand.randint(0, 370)
      point+=1
      coin = font.render("coin: " +str(point), True, "black")
    # player coords update
    pygame.draw.rect(screen, f"{player_colour}", (x, y, 50, 50))
    # coin coords and amount update
    pygame.draw.rect(screen, "yellow", (x1, y1, 30, 30))
    screen.blit(coin, (0,0))
    # esc button update
    pygame.draw.rect(screen, "grey", esc)
    pygame.draw.rect(screen, "green" if esc.collidepoint(pygame.mouse.get_pos()) else "grey", esc)
    fonto = pygame.font.Font(None, 24)
    esc_text = fonto.render("esc", True, "black")
    coords = esc_text.get_rect(center = esc.center)
    screen.blit(esc_text, coords)
      
  
      
    
    
      
    
  pygame.display.flip()
  clock.tick(60)