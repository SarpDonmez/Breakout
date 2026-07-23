#Imports Pygame
import pygame

#Imports random
import random

#Variables for screen size
screen_width = 800
screen_height = 800

#Initialize Pygame 
pygame.init()
#Creating the game window 
screen = pygame.display.set_mode((screen_width, screen_height))
#Hide Mouse Cursor
pygame.mouse.set_visible(False)
#Game clock to control framerate
clock = pygame.time.Clock()

def create_player():
     '''Function that creates the rectangle the player controls'''
     player = pygame.Rect(0, 0, 120, 20)
     player.center = (screen_width//2, screen_height*0.9)
     return player

def create_bricks(rows=8, columns=10, brick_width=65, brick_height=25, brick_distance=5):
     '''Function that creates the grid'''
     bricks = []
     for row in range(rows):
          for col in range(columns):
               x = (col * (brick_width + brick_distance)) + 53
               y = (row * (brick_height + brick_distance)) + 100
               brick = pygame.Rect(x, y , brick_width, brick_height)
               bricks.append(brick)
     return bricks

def create_ball():
     '''Function to create the game ball'''
     ball = pygame.Rect(0, 0, 25, 25)
     ball.center = (screen_width//2, screen_height//2 + 50)
     return ball

def display_text(text, color):
     '''Function to display a message on the screen'''
     screen.fill((0,0,0))
     font = pygame.font.Font(None, 100)
     text = font.render(text, True, color)
     text_rect = text.get_rect(center=(screen_width//2, screen_height//2))
     screen.blit(text, text_rect)
     pygame.display.flip()
     pygame.time.delay(2000)

def ball_wall_collisions(ball, speedx, speedy, running):
     '''Function that handles ball-wall collisions'''
     #Wall Bounce
     if ball.left <= 0 or ball.right >= screen_width:
          speedx *= -1
     if ball.top <= 0:
          speedy *= -1
     if ball.bottom >= screen_height:
          display_text("GAME OVER!", (255, 0, 0))
          running = False
     return speedx, speedy, running

def run(difficulty = 1):
     '''Main function for the running loop of the game'''
     #Variables for the game loop
     running = True
     player = create_player()
     bricks = create_bricks()
     ball = create_ball()
     max_speedx = 8 * difficulty 
     ball_speedx = random.choice([-max_speedx, max_speedx])
     ball_speedy = -4 * difficulty

     #Main game loop 
     while running:
          keys = pygame.key.get_pressed()

          #Player movement based on right and left arrow keys
          if keys[pygame.K_RIGHT]:
               player.centerx += 8
          if keys[pygame.K_LEFT]:
               player.centerx -= 8


          player.centerx = max(player.width//2, player.centerx)
          player.centerx = min(screen_width - player.width // 2, player.centerx)
    
          screen.fill((0,0,0))
          pygame.draw.rect(screen, (0, 255, 0), player)
          pygame.draw.ellipse(screen, (255, 255, 255), ball)
          for brick in bricks:
               pygame.draw.rect(screen, (255,0,0), brick)
        
          ball.x += ball_speedx
          ball.y += ball_speedy

          #Wall collisions
          ball_speedx, ball_speedy, running = ball_wall_collisions(ball, ball_speedx, ball_speedy, running)


          #Player Bounce
          if ball.colliderect(player):
               if ball.bottom - ball_speedy <= player.top:
                    ball.bottom = player.top 
                    offset = (ball.centerx - player.centerx) / (player.width / 2)  
                    ball_speedx = offset * max_speedx
                    ball_speedy *= -1
               else:
                    if ball.centerx < player.centerx:
                         ball.right = player.left
                    else:
                         ball.left = player.right
                    ball_speedx *= -1

          if not bricks:
               display_text("YOU WIN!", (0, 255, 0))
               running = False

          #Brick bounce
          for brick in bricks[:]:
               if ball.colliderect(brick):
                    if ball.bottom - ball_speedy <= brick.top or ball.top - ball_speedy >= brick.bottom:
                         ball_speedy *= -1
                    elif ball.right - ball_speedx <= brick.left or ball.left - ball_speedx >= brick.right:
                         ball_speedx *= -1
                    bricks.remove(brick)
                    break

          pygame.display.flip()
          clock.tick(60)
        
          for event in pygame.event.get():
               if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                         running = False

#Calling the run function 
run()