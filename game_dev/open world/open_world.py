import sys
import pygame
import random as rand

pygame.init()
# player coords
player_x = 245
player_y = 245

# player effects
player_speed = 5
player_health = 5
# screen
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("The underground")

# camera
camera_x = 0
camera_y = 0

#ground png
ground = pygame.image.load("ground.png")
ground = pygame.transform.scale(ground, (500, 500))

#clock
clock = pygame.time.Clock()

#x y history
x_history = [0, 499]
y_history = [0, 499]

#player coords
font = pygame.font.Font(None, 30)

# chunk check coords
check_x = []
check_y = []

#chest image
chest = pygame.image.load("chest.png")
chest = pygame.transform.scale(chest, (30, 30))
#player move
def move():
  global player_x, player_y, player_speed, camera_x, camera_y
  keys = pygame.key.get_pressed()
  if keys[pygame.K_w] and ((player_y-camera_y-player_speed>15 and player_x-camera_x<130) or (player_y-camera_y-player_speed>15 and player_x-camera_x>370) or (player_x-camera_x>130 and player_x-camera_x<370)):
    player_y -= player_speed
  if keys[pygame.K_s] and ((player_y-camera_y+player_speed<475 and player_x-camera_x<130) or (player_y-camera_y+player_speed<475 and player_x-camera_x>370) or (player_x-camera_x>130 and player_x-camera_x<370)):
    player_y += player_speed
  if keys[pygame.K_a] and ((player_x-camera_x-player_speed>15 and player_y-camera_y<130) or (player_x-camera_x-player_speed>15 and player_y-camera_y>370) or (player_y-camera_y>130 and player_y-camera_y<370)):
    player_x -= player_speed
  if keys[pygame.K_d] and ((player_x-camera_x+player_speed<475 and player_y-camera_y<130) or (player_x-camera_x+player_speed<475 and player_y-camera_y>370) or (player_y-camera_y>130 and player_y-camera_y<370)):
    player_x +=player_speed
    
#entities in chunk 
mob_x = []
mob_y = []

#check and generate the chunk
def gen():
  global check_x, check_y, camera_x, camera_y, mob_x, mob_y
  contains_a_chest = rand.randint(1, 4)
  if contains_a_chest == 2:
    x = rand.randint(camera_x+36, camera_x+465)
    y = rand.randint(camera_y+36, camera_y+465)
    mob_x.append(x)
    mob_y.append(y)
  check_x.append(camera_x+5)
  check_y.append(camera_y+5)


  
#main
while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
  
  #player
  move()
  
  #camera x y update
  if player_x < x_history[0]:
    camera_x -= 500
    x_history[0] -= 500
    x_history[1] -= 500
  if player_y < y_history[0]:
    camera_y -= 500
    y_history[0] -= 500
    y_history[1] -= 500
  if player_x > x_history[1]:
    camera_x += 500
    x_history[0] += 500
    x_history[1] += 500
  if player_y > y_history[1]:
    camera_y += 500
    y_history[0] += 500
    y_history[1] += 500
    
  #pov
  camera = pygame.Surface(screen.get_size())
  camera.fill("brown")
  camera.blit(ground, (0, 0))
  pygame.draw.rect(camera, "black", (player_x-camera_x, player_y-camera_y, 10, 10))

  #check if loaded the chunk
  if camera_x+5 not in check_x or camera_y+5 not in check_y:
    gen()
  else:
    #load the chunk
    for i in range(len(mob_x)):
      if mob_x[i] > camera_x and mob_x[i] < camera_x+500 and mob_y[i] > camera_y and mob_y[i] <camera_y+500:
        camera.blit(chest, (mob_x[i]-camera_x, mob_y[i]-camera_y))
  #player coords
  player_coords = font.render(f"x:{player_x} y:{player_y}", True, "white")
  camera.blit(player_coords, (20, 20))
  
  #the wall
  pygame.draw.rect(camera, "grey", (0, 0, 15, 130))
  pygame.draw.rect(camera, "grey", (0, 0, 130, 15))
  
  pygame.draw.rect(camera, "grey", (0, 485, 130, 15))
  pygame.draw.rect(camera, "grey", (0, 370, 15, 130))
  
  pygame.draw.rect(camera, "grey", (485, 0, 15, 130))
  pygame.draw.rect(camera, "grey", (370, 0, 130, 15))

  pygame.draw.rect(camera, "grey", (485, 370, 15, 130))
  pygame.draw.rect(camera, "grey", (370, 485, 130, 15))

  

  
  screen.blit(camera, (0, 0))
  
  pygame.display.flip()
  clock.tick(60)