from sys import exit

import pygame
import sys
import random


# Classes

class Boat(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("venv/assets/boat.png")
        self.image = pygame.transform.rotozoom(self.image, 180, 0.3)
        self.rect = self.image.get_rect(center=(800, 640))
        self.mask = pygame.mask.from_surface(self.image)

    def player_input(self, direction):
        if direction == 'left':
            self.rect.x -= 12.5
        elif direction == 'right':
            self.rect.x += 12.5

        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > 1329.4:
            self.rect.x = 1329.4

    def update(self, move, left):
        if move:
            self.player_input(left)


class Plastic(pygame.sprite.Sprite):
    def __init__(self, type,speed):
        super().__init__()
        if type == "plastic_bag":
            self.image = pygame.image.load("venv/assets/plasticbag.png").convert_alpha()
            self.image = pygame.transform.rotozoom(self.image, 0, 0.2)

        elif type == "plastic_wrap":
            self.image = pygame.image.load("venv/assets/plasticwrap.png").convert_alpha()
            self.image = pygame.transform.rotozoom(self.image, 0, 0.2)

        self.rect = self.image.get_rect(center=(random.randint(0, 1600), -40))
        self.mask = pygame.mask.from_surface(self.image)
        self.drop_speed = speed

    def destroy(self):
        if self.rect.y >= 900:
            self.kill()

    def update(self):
        self.destroy()
        self.rect.y += self.drop_speed

class Fish(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("venv/assets/fish.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.3)
        self.rect = self.image.get_rect(center=(random.randint(0, 1600), -40))
        self.mask = pygame.mask.from_surface(self.image)

    def destroy(self):
        if self.rect.y >= 900:
            self.kill()

    def update(self):
        self.destroy()
        self.rect.y += 5

class Buttons:
    def __init__(self, position, image,scale):
        self.surface = pygame.image.load(image).convert_alpha()
        self.surface = pygame.transform.rotozoom(self.surface, 0, scale)
        self.rect = self.surface.get_rect(center=position)
        self.mask = pygame.mask.from_surface(self.surface)

def plastic_collison_detector():
  for i in plastic_group:
    if i.mask.overlap(boat.sprite.mask,(boat.sprite.rect.x - i.rect.x, boat.sprite.rect.y - i.rect.y)):
      i.kill()
      sfx4.play()
      return 1
  return 0

def fish_collison_detector():
  for i in fish_group:
    if i.mask.overlap(boat.sprite.mask,(boat.sprite.rect.x - i.rect.x, boat.sprite.rect.y - i.rect.y)):
      fish_group.empty()
      plastic_group.empty()
      sfx1.play()
      sfx2.play()
      sfx3.play()
      return 'Menu'
    else:
       pass

  return 'Play'

def plastic_off_screen():
  for i in plastic_group:
    if i.rect.y >= 900:
      i.kill()
      return 1
  return 0

pygame.init()
screen = pygame.display.set_mode((1600, 900))
pygame.display.set_caption('Capture the Trash')
clock = pygame.time.Clock()

bg_menu = pygame.image.load('venv/assets/gradient.png').convert()
bg_menu_rect = bg_menu.get_rect(topleft=(0, 0))

bg_game = pygame.image.load('venv/assets/background.png').convert()
bg_game = pygame.transform.rotozoom(bg_game, 0, 2.62)
bg_game_rect = bg_game.get_rect(topleft=(0, 0))

game_font = pygame.font.Font('venv/assets/GloriaHallelujah-Regular.ttf', 50)

# Main menu text
welcome_message = game_font.render('BIG PLASTIC FISHERS', False, 'white')
welcome_message_rect = welcome_message.get_rect(center=(800, 90))
welcome_message1 = game_font.render('1. Move your boat around using arrow keys.', False, 'white')
welcome_message1_rect = welcome_message1.get_rect(center=(800, 200))
welcome_message2 = game_font.render('2. Collect as many pieces of trash as possible.', False, 'white')
welcome_message2_rect = welcome_message2.get_rect(center=(800, 275))
welcome_message3 = game_font.render('3. Avoid hitting the fish.', False, 'white')
welcome_message3_rect = welcome_message3.get_rect(center=(800, 350))
welcome_message4 = game_font.render('4. Have fun!', False, 'white')
welcome_message4_rect = welcome_message3.get_rect(center=(1000, 425))

# Information screen text
info_message1 = game_font.render('This is our coding project to raise awareness', False, 'white')
info_message1_rect = info_message1.get_rect(center=(800, 200))
info_message2 = game_font.render('about the environment, in specific, plastic pollution', False, 'white')
info_message2_rect = info_message2.get_rect(center=(800, 275))
info_message3 = game_font.render('Our game promotes the idea of cleaning up our oceans', False, 'white')
info_message3_rect = info_message3.get_rect(center=(800, 350))
info_message4 = game_font.render('whilst avoiding fish to reduce the effect of overfishing', False, 'white')
info_message4_rect = info_message4.get_rect(center=(800, 425))

score = 0
high_score = 0
game_active = 'Menu'

boat = pygame.sprite.GroupSingle()
boat.add(Boat())

plastic_group = pygame.sprite.Group()
fish_group = pygame.sprite.Group()

# Main menu buttons
start_button = Buttons((800, 750), 'venv/assets/start.png',1)
back_button = Buttons((200, 800), 'venv/assets/back.png',1)
info_button = Buttons((800, 550), 'venv/assets/info.png',1.2)

# Spawning rates
plastic_spawning_rate = 2000  # 2000 milliseconds means 2 seconds
plastic_spawn = pygame.USEREVENT + 1

fish_spawning_rate = 4000  # 2000 milliseconds means 2 seconds
fish_spawn = pygame.USEREVENT + 2
pygame.time.set_timer(fish_spawn, fish_spawning_rate)
pygame.time.set_timer(plastic_spawn, plastic_spawning_rate)

# Sound effects
sfx1 = pygame.mixer.Sound('venv/assets/BOOM sound effect.mp3')
sfx1.set_volume(0.2)
sfx2 = pygame.mixer.Sound('venv/assets/Fortnite Death Sound Effect (No copyright).mp3')
sfx2.set_volume(0.2)
sfx3 = pygame.mixer.Sound('venv/assets/Wah Wah Wahhhh (Sound Effect).mp3')
sfx3.set_volume(0.2)
sfx4 = pygame.mixer.Sound('venv/assets/Cash Register (Kaching) - Sound Effect (HD).mp3')
sfx4.set_volume(0.2)

# Background music
bg_music = pygame.mixer.Sound('venv/assets/Fortnite Coral Chorus Lobby Music Pack.mp3')
bg_music.set_volume(0.2)
bg_music.play(loops=-1)

drop_speed = 5



while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active == 'Play':
            if event.type == plastic_spawn:
                plastic_object = Plastic(random.choice(['plastic_bag', 'plastic_wrap']),drop_speed)
                plastic_group.add(plastic_object)
                pygame.time.set_timer(plastic_spawn, int(plastic_spawning_rate))
            if event.type == fish_spawn:
                fish_object = Fish()
                fish_group.add(fish_object)

    # Anything that happens when the player presses start goes in this loop
    if game_active == 'Play':

        screen.blit(bg_game, bg_game_rect)
        score_message = game_font.render(f'Score: {score}', False, 'white')
        score_message_rect = score_message.get_rect(center=(110, 50))
        screen.blit(score_message,score_message_rect)
        boat.update(False, False)
        boat.draw(screen)

        if plastic_spawning_rate >= 500:
            plastic_spawning_rate -= 0.5

        drop_speed += 0.001

        score += plastic_collison_detector()
        score -= plastic_off_screen()
        game_active = fish_collison_detector()

        plastic_group.draw(screen)
        plastic_group.update()
        fish_group.draw(screen)
        fish_group.update()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            boat.update(True, 'left')
        if keys[pygame.K_RIGHT]:
            boat.update(True, 'right')
    # Anything that happens in menu screen goes here
    elif game_active == 'Menu':
        drop_speed = 5
        plastic_spawning_rate = 2000
        screen.blit(bg_menu, bg_menu_rect)
        screen.blit(start_button.surface, start_button.rect)
        screen.blit(info_button.surface, info_button.rect)
        screen.blit(welcome_message, welcome_message_rect)
        if score == 0:
            screen.blit(welcome_message1, welcome_message1_rect)
            screen.blit(welcome_message2, welcome_message2_rect)
            screen.blit(welcome_message3, welcome_message3_rect)
            screen.blit(welcome_message4, welcome_message4_rect)
        else:
            final_score_message = game_font.render(f'Your score: {score}', False, 'white')
            final_score_message_rect = final_score_message.get_rect(center=(800, 300))
            screen.blit(final_score_message, final_score_message_rect)
            if score > high_score:
                high_score = score
            high_score_message = game_font.render(f'High Score: {high_score}', False, 'white')
            high_score_message_rect = high_score_message.get_rect(center=(800, 400))
            screen.blit(high_score_message, high_score_message_rect)
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if start_button.rect.collidepoint(pos) and start_button.mask.get_at(
                    (pos[0] - start_button.rect.x, pos[1] - start_button.rect.y)):
                game_active = 'Play'
                score = 0
            elif info_button.rect.collidepoint(pos):
                game_active = 'Info'
    else:
        screen.blit(bg_menu, bg_menu_rect)
        screen.blit(welcome_message, welcome_message_rect)
        screen.blit(info_message1, info_message1_rect)
        screen.blit(info_message2, info_message2_rect)
        screen.blit(info_message3, info_message3_rect)
        screen.blit(info_message4, info_message4_rect)
        screen.blit(back_button.surface, back_button.rect)
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if back_button.rect.collidepoint(pos):
                game_active = 'Menu'

    pygame.display.update()
    clock.tick(60)
