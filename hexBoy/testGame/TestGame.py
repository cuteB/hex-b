import pygame
import random

from pygame.locals import (
  K_UP,
  K_DOWN,
  K_LEFT,
  K_RIGHT,
  K_ESCAPE,
  KEYDOWN,
  QUIT,
)

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

''' Player sprite '''
class Player(pygame.sprite.Sprite):
  def __init__(self):
    super(Player, self).__init__()
    self.surf = pygame.Surface((75, 25))
    self.surf.fill((255, 255, 255))
    self.rect = self.surf.get_rect()

  def update(self, pressed_keys):
    if pressed_keys[K_UP]:
      self.rect.move_ip(0, -5)
    if pressed_keys[K_DOWN]:
      self.rect.move_ip(0, 5)
    if pressed_keys[K_LEFT]:
      self.rect.move_ip(-5, 0)
    if pressed_keys[K_RIGHT]:
      self.rect.move_ip(5, 0)

    # Keep player on screen
    if self.rect.left < 0:
      self.rect.left = 0
    if self.rect.right > SCREEN_WIDTH:
      self.rect.right = SCREEN_WIDTH
    if self.rect.top <= 0:
      self.rect.top = 0
    if self.rect.bottom >= SCREEN_HEIGHT:
      self.rect.bottom = SCREEN_HEIGHT

''' Enemy Sprite '''
class Enemy(pygame.sprite.Sprite):
  def __init__(self):
    super(Enemy, self).__init__()
    self.surf = pygame.Surface((20, 10))
    self.surf.fill((255, 255, 255))
    self.rect = self.surf.get_rect(
      center = (
        random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
        random.randint(0, SCREEN_HEIGHT)
      )
    )
    self.speed = random.randint(5,20)

  def update(self):
    self.rect.move_ip(-self.speed, 0)
    if self.rect.right < 0:
      self.kill()

def TestGame_main():
  pygame.init()

  # Create game screen
  screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

  # create event for adding a new enemy
  ADDENEMY = pygame.USEREVENT + 1
  pygame.time.set_timer(ADDENEMY, 250)

  # Create Player
  player = Player()

  # Create enemies
  enemies = pygame.sprite.Group()
  all_sprites = pygame.sprite.Group()
  all_sprites.add(player)

  # game clock
  clock = pygame.time.Clock()

  '''
  Game loop
  1. Processes user input
  2. Updates the state of all game objects
  3. Updates the display and audio ouput
  4. Maintains the speed of the game
  '''
  running = True
  while running:
    # Look at events in the queue
    for event in pygame.event.get():
      #user hit a key?
      if event.type == KEYDOWN:
        # Check if it was the escape key
        if event.key == K_ESCAPE:
          running = False

      # user clicked the close button
      elif event.type == QUIT:
        running = False

      # add new enemy
      elif event.type == ADDENEMY:
        new_enemy = Enemy()
        enemies.add(new_enemy)
        all_sprites.add(new_enemy)

    # update player
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    # update enemy
    enemies.update()

    #-------------------------------------------
    # Screen stuff
    #-------------------------------------------
    # make screen black
    screen.fill((0, 0, 0))

    # draw sprites
    for entity in all_sprites:
      screen.blit(entity.surf, entity.rect)

    # check if any enemies have collided with playey
    if pygame.sprite.spritecollideany(player, enemies):
      player.kill()
      running = False

    # render
    pygame.display.flip()

    # maintain 30 fps
    clock.tick(30)

  #-------------------------------------------
  # End running loop
  #-------------------------------------------
  pygame.quit()
