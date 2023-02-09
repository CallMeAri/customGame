from sys import exit
from random import randint
import pygame
def display_score():
    current_time = int(pygame.time.get_ticks() / 1000)- start_time
    score_surf = test_font.render(f'Score: {current_time}',False,(64, 64, 64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf, score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 250:
                screen.blit(snail_surf, obstacle_rect)
            else:
                screen.blit(fly_surf, obstacle_rect)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else: return []

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True

def player_animation():
    global player_surf, player_index

    if player_rect.bottom < 250:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):player_index = 0
        player_surf = player_walk[int(player_index)]
pygame.init()

screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Snail Jump')
clock = pygame.time.Clock()

test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

win_text = test_font.render('You Win!', False, (64, 64, 64))
win_rect = win_text.get_rect(center = (400, 50))

lose_text = test_font.render('You Lose!', False, (64, 64, 64))
lose_rect = lose_text.get_rect(center = (400, 50))

game_active = False
start_time = 0
score = 0

player = pygame.sprite.GroupSingle()
#score_surf = test_font.render('Score', False, (64, 64 ,64))
#score_rect = score_surf.get_rect(center = (400, 50))
sky_surface = pygame.image.load('graphics/Sky.png')
ground_surface = pygame.image.load('graphics/ground.png')



snail_frame_1= pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_index = 0
snail_surf = snail_frames[snail_index]
snail_x_pos = 600
snail_rect = snail_surf.get_rect(midbottom = (snail_x_pos, 250))

fly_walk_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
fly_walk_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
fly_walk = [fly_walk_1, fly_walk_2]
fly_index = 0
fly_surf = fly_walk[fly_index]
fly_rect = fly_surf.get_rect(center = (randint(900, 1000), 100))
obstacle_rect_list = []

player_sneak = pygame.image.load('graphics/player/player_sneak_1.png').convert_alpha()
player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2, player_sneak]
player_index = 0
player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (80, 250))
player_gravity = 0
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand_scaled = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand_scaled.get_rect(center = (400, 200))

game_name = test_font.render('Snail Jumper', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center = (400, 50))

game_message = test_font.render('Press space to play', False, (111, 196, 169))
game_message_rect = game_message.get_rect(center = (400, 340))
cloud_base = pygame.Surface((40, 10))
cloud_base.fill('white')

cloud_cap = pygame.Surface((20, 10))
cloud_cap.fill('white')

cloud_shadow = pygame.Surface((10, 5))
cloud_shadow.fill('azure2')

dirt_image = pygame.Surface((5, 5))
dirt_image.fill('grey')

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1300)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT:
                    player_surf = pygame.image.load('graphics/player/player_sneak_1.png').convert_alpha()
                if event.key == pygame.K_a:
                    player_rect.x -= 5
                    player_surf = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
                if event.key == pygame.K_d:
                    player_rect.x += 5
                    player_surf = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if player_rect.bottom == 250:
                        player_gravity = -20
                        player_surf = pygame.image.load('graphics/player/jump.png').convert_alpha()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos):
                    player_gravity = -20
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT:
                    player_rect.y -= 1
                    player_surf = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
                if event.key == pygame.K_a:
                    player_surf = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
                if event.key == pygame.K_d:
                    player_surf = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
                if event.key == pygame.K_SPACE and  player_rect.bottom > 250:
                    player_surf = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                snail_rect.left = 800
                start_time = int(pygame.time.get_ticks() / 1000)
        if game_active:

            if event.type == obstacle_timer:
                if randint(0, 2):
                    obstacle_rect_list.append(snail_surf.get_rect(midbottom = (randint(900, 1000), 250)))
                else:
                    obstacle_rect_list.append(fly_surf.get_rect(center = (randint(900, 1000), 100)))
            if event.type == snail_animation_timer:
                if snail_index == 0: snail_index = 1
                else: snail_index = 0
                snail_surf = snail_frames[snail_index]
            if event.type == fly_animation_timer:
                if fly_index == 0: fly_index = 1
                else: fly_index = 0
                fly_surf = fly_walk[fly_index]
    # draw all our elements
    # update everything
    if game_active:
        screen.blit(sky_surface,(0, 0))
        screen.blit(ground_surface,(0, 250))
        screen.blit(dirt_image, (10, 300))
        screen.blit(dirt_image, (20, 390))
        screen.blit(dirt_image, (30, 350))
        screen.blit(dirt_image, (50, 320))
        screen.blit(dirt_image, (70, 330))
        screen.blit(dirt_image, (90, 380))

        screen.blit(cloud_base, (100, 100))
        screen.blit(cloud_cap, (110, 90))
        screen.blit(cloud_shadow, (100, 95))
        screen.blit(cloud_shadow, (130, 95))

        screen.blit(dirt_image, (110, 300))
        screen.blit(dirt_image, (120, 390))
        screen.blit(dirt_image, (130, 350))
        screen.blit(dirt_image, (150, 320))
        screen.blit(dirt_image, (170, 330))
        screen.blit(dirt_image, (190, 380))

        screen.blit(cloud_base, (200, 50))
        screen.blit(cloud_cap, (210, 40))
        screen.blit(cloud_shadow, (200, 45))
        screen.blit(cloud_shadow, (230, 45))

        screen.blit(dirt_image, (210, 300))
        screen.blit(dirt_image, (220, 390))
        screen.blit(dirt_image, (230, 350))
        screen.blit(dirt_image, (250, 320))
        screen.blit(dirt_image, (270, 330))
        screen.blit(dirt_image, (290, 380))

        screen.blit(cloud_base, (300, 150))
        screen.blit(cloud_cap, (310, 140))
        screen.blit(cloud_shadow, (300, 145))
        screen.blit(cloud_shadow, (330, 145))

        screen.blit(dirt_image, (310, 300))
        screen.blit(dirt_image, (320, 390))
        screen.blit(dirt_image, (330, 350))
        screen.blit(dirt_image, (350, 320))
        screen.blit(dirt_image, (370, 330))
        screen.blit(dirt_image, (390, 380))

        screen.blit(cloud_base, (400, 130))
        screen.blit(cloud_cap, (410, 120))
        screen.blit(cloud_shadow, (400, 125))
        screen.blit(cloud_shadow, (430, 125))

        screen.blit(dirt_image, (410, 300))
        screen.blit(dirt_image, (420, 390))
        screen.blit(dirt_image, (430, 350))
        screen.blit(dirt_image, (450, 320))
        screen.blit(dirt_image, (470, 330))
        screen.blit(dirt_image, (490, 380))

        screen.blit(cloud_base, (500, 30))
        screen.blit(cloud_cap, (510, 20))
        screen.blit(cloud_shadow, (500, 25))
        screen.blit(cloud_shadow, (530, 25))

        screen.blit(dirt_image, (510, 300))
        screen.blit(dirt_image, (520, 390))
        screen.blit(dirt_image, (530, 350))
        screen.blit(dirt_image, (550, 320))
        screen.blit(dirt_image, (570, 330))
        screen.blit(dirt_image, (590, 380))

        screen.blit(cloud_base, (600, 70))
        screen.blit(cloud_cap, (610, 60))
        screen.blit(cloud_shadow, (600, 65))
        screen.blit(cloud_shadow, (630, 65))

        screen.blit(dirt_image, (610, 300))
        screen.blit(dirt_image, (620, 390))
        screen.blit(dirt_image, (630, 350))
        screen.blit(dirt_image, (650, 320))
        screen.blit(dirt_image, (670, 330))
        screen.blit(dirt_image, (690, 380))

        screen.blit(dirt_image, (710, 300))
        screen.blit(dirt_image, (720, 390))
        screen.blit(dirt_image, (730, 350))
        screen.blit(dirt_image, (750, 320))
        screen.blit(dirt_image, (770, 330))
        screen.blit(dirt_image, (790, 380))
        pygame.draw.ellipse(screen, '#c0e8ec', pygame.Rect(350, 0, 100, 100))
      #  screen.blit(score_surf, score_rect)
        screen.blit(snail_surf, snail_rect)
        score = display_score()

    #player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom > 250:player_rect.bottom = 250
        player_animation()
        screen.blit(player_surf, player_rect)
        player.draw(screen)
        player.update()
    #obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

     # keys = pygame.key.get_pressed()
     # if keys[pygame.K_SPACE]:
     #    print('jump')
        snail_rect.x -= 5


     #  if((player_rect.colliderect(snail_rect)) == 1):
     #      pygame.quit()
      #      exit()
      # mouse_pos = pygame.mouse.get_pos()
     #  if player_rect.collidepoint(mouse_pos):
     #      print(pygame.mouse.get_pressed())


        game_active = collisions(player_rect, obstacle_rect_list)
    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand_scaled, player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80, 250)
        player_gravity = 0
        score_message = test_font.render(f'Your score: {score}', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center = (400, 330))
        screen.blit(game_name, game_name_rect)
        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)
    pygame.display.update()
    clock.tick(60)

