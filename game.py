import pygame
import random
import sys


# PYGAME.ORG HAS ALL THE PYGAME METHODS!!

pygame.init()

WIDTH = 800
HEIGHT = 600

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BACKGROUND_COLOR = (0, 0, 0)

# (0, 0) coordinate is top left
player_size = 50
player_pos = [int(WIDTH/2), int(HEIGHT - 2*player_size)]

enemy_size = 50
enemy_pos = [int((random.randint(0, WIDTH-enemy_size))), 0]
enemy_list = [enemy_pos]

SPEED = 10

myFont = pygame.font.SysFont("monospace", 35)

SCORE = 0


#creates a screen for your game
#you passed a tuple into set_mode
# (800, 600) is a tuple
screen = pygame.display.set_mode((WIDTH, HEIGHT))

game_over = False

clock = pygame.time.Clock()

def set_level(SCORE, SPEED):
    if SCORE < 20:
        SPEED = 5
    elif SCORE < 40:
        SPEED = 8
    elif SCORE < 60:
        SPEED = 12
    elif SCORE < 80:
        SCORE = 15
    else:
        SPEED = 15
    return SPEED

def drop_enemies(enemy_list):

    delay = random.random()
    if len(enemy_list) < 10 and delay < 0.1:
        x_pos = random.randint(0, WIDTH - enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])

def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        pygame.draw.rect(screen, BLUE, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))

def update_enemy_positions(enemy_list, SCORE):

    for idx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and enemy_pos[1] < HEIGHT:
            enemy_pos[1] += SPEED
        else:
            SCORE += 1
            enemy_list.pop(idx)
    return SCORE

def collision_check(enemy_list, player_pos):
    for enemy_pos in enemy_list:
        if detect_collision(enemy_pos, player_pos):
            return True
    return False

def detect_collision(player_pos, enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    e_x = enemy_pos[0]
    e_y = enemy_pos[1]

    if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x + enemy_size)):
        if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y + enemy_size)):
            return True
    else:
        return False


# make a GAME LOOP AS FOLLOWS
# with a while loop and a for loop
while not game_over:

    # this for loops designed to handle operations that consider events that occur in the pygame
    for event in pygame.event.get():
        # SUPER IMPORT IF STATEMENT TO ALLOW YOU TO X OUT OF A GAME
        if event.type == pygame.QUIT:
            sys.exit()

        # moves player
        if event.type == pygame.KEYDOWN:

            x = player_pos[0]
            y = player_pos[1]

            if event.key == pygame.K_LEFT:
                x -= player_size
            elif event.key == pygame.K_RIGHT:
                x += player_size

            player_pos = [x, y]

        #just to see what is going on
        print(event)

    # fill screen black on each frame so we fully update each frame
    screen.fill(BACKGROUND_COLOR)

    # draws a rectangle. 2nd parameter is RGB color, 3rd is parameters that define rectangle object
    # nice to have vars
    drop_enemies(enemy_list)
    SCORE = update_enemy_positions(enemy_list, SCORE)
    SPEED = set_level(SCORE, SPEED)

    text = "Score: " + str(SCORE)
    label = myFont.render(text, 1, YELLOW)
    screen.blit(label, (WIDTH-200, HEIGHT-40))

    if collision_check(enemy_list, player_pos):
        game_over = True
        break
    draw_enemies(enemy_list)


    pygame.draw.rect(screen, RED, (player_pos[0], player_pos[1], player_size, player_size))

    clock.tick(30)
    # updates the display on every loop, otherwise you can't see anything new
    pygame.display.update()

print("GAME OVER!\nYOUR SCORE WAS: " + str(SCORE))


