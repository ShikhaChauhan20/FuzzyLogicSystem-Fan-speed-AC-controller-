import random
import sys
import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Python Dungeon Crawler - Ultimate Edition")

clock = pygame.time.Clock()

player_size = 40
player_x = 150
player_y = 150
player_speed = 5

enemy_size = 35
enemy_x = 550
enemy_y = 400
enemy_speed = 2

walls = [
    pygame.Rect(100, 100, 600, 20),
    pygame.Rect(100, 100, 20, 400),
    pygame.Rect(680, 100, 20, 400),
    pygame.Rect(100, 480, 600, 20),
]

treasure = pygame.Rect(
    random.randint(130, 630), random.randint(130, 430), 30, 30
)
score = 0
font = pygame.font.SysFont(None, 36)

running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  keys = pygame.key.get_pressed()
  dx, dy = 0, 0
  if keys[pygame.K_a] or keys[pygame.K_LEFT]:
    dx = -player_speed
  if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
    dx = player_speed
  if keys[pygame.K_w] or keys[pygame.K_UP]:
    dy = -player_speed
  if keys[pygame.K_s] or keys[pygame.K_DOWN]:
    dy = player_speed

  player_x += dx
  player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
  for wall in walls:
    if player_rect.colliderect(wall):
      if dx > 0:
        player_x = wall.left - player_size
      if dx < 0:
        player_x = wall.right

  player_y += dy
  player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
  for wall in walls:
    if player_rect.colliderect(wall):
      if dy > 0:
        player_y = wall.top - player_size
      if dy < 0:
        player_y = wall.bottom

  if enemy_x < player_x:
    enemy_x += enemy_speed
  elif enemy_x > player_x:
    enemy_x -= enemy_speed

  if enemy_y < player_y:
    enemy_y += enemy_speed
  elif enemy_y > player_y:
    enemy_y -= enemy_speed

  enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_size, enemy_size)
  if player_rect.colliderect(enemy_rect):
    score = max(0, score - 1)
    enemy_x, enemy_y = 550, 400

  if treasure and player_rect.colliderect(treasure):
    score += 1
    treasure = pygame.Rect(
        random.randint(130, 630), random.randint(130, 430), 30, 30
    )

  screen.fill((30, 30, 30))

  for wall in walls:
    pygame.draw.rect(screen, (100, 100, 100), wall)

  if treasure:
    pygame.draw.rect(screen, (255, 215, 0), treasure)

  pygame.draw.rect(screen, (50, 150, 255), enemy_rect)
  pygame.draw.rect(
      screen, (200, 50, 50), (player_x, player_y, player_size, player_size)
  )

  score_text = font.render(f"Score: {score}", True, (255, 255, 255))
  screen.blit(score_text, (120, 120))

  pygame.display.flip()
  clock.tick(FPS)

pygame.quit()
sys.exit()