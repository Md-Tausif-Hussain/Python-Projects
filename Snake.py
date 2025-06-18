import pygame
import time
import random
import os

# Initialize
pygame.init()

# Screen setup
width, height = 600, 400
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game 🐍")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (213, 50, 80)
blue = (50, 153, 213)
grey = (200, 200, 200)

# Snake settings
block_size = 20
initial_speed = 10

# Fonts
font = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 30)

# High Score File
high_score_file = "high_score.txt"
if not os.path.exists(high_score_file):
    with open(high_score_file, "w") as f:
        f.write("0")

def load_high_score():
    with open(high_score_file, "r") as f:
        return int(f.read())

def save_high_score(score):
    if score > load_high_score():
        with open(high_score_file, "w") as f:
            f.write(str(score))

def draw_grid():
    for x in range(0, width, block_size):
        pygame.draw.line(win, grey, (x, 0), (x, height))
    for y in range(0, height, block_size):
        pygame.draw.line(win, grey, (0, y), (width, y))

def draw_snake(snake_list):
    for pos in snake_list:
        pygame.draw.rect(win, green, [pos[0], pos[1], block_size, block_size])

def show_score(score, high_score, level):
    text = score_font.render(f"Score: {score}  High Score: {high_score}  Level: {level}", True, white)
    win.blit(text, [10, 10])

def game_loop():
    game_over = False
    pause = False

    x, y = width // 2, height // 2
    dx, dy = 0, 0
    snake = []
    length = 1
    speed = initial_speed

    food_x = random.randrange(0, width - block_size, block_size)
    food_y = random.randrange(0, height - block_size, block_size)

    clock = pygame.time.Clock()
    high_score = load_high_score()

    while not game_over:
        while pause:
            win.fill(black)
            msg = font.render("Paused. Press P to Resume", True, red)
            win.blit(msg, [width // 4, height // 2])
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    pause = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and dx == 0:
                    dx, dy = -block_size, 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx, dy = block_size, 0
                elif event.key == pygame.K_UP and dy == 0:
                    dx, dy = 0, -block_size
                elif event.key == pygame.K_DOWN and dy == 0:
                    dx, dy = 0, block_size
                elif event.key == pygame.K_p:
                    pause = True

        # Move snake
        x += dx
        y += dy

        # ✅ Wrap-Around Logic
        if x >= width:
            x = 0
        elif x < 0:
            x = width - block_size
        if y >= height:
            y = 0
        elif y < 0:
            y = height - block_size

        head = [x, y]
        snake.append(head)
        if len(snake) > length:
            del snake[0]

        if head in snake[:-1]:
            break

        if x == food_x and y == food_y:
            length += 1
            food_x = random.randrange(0, width - block_size, block_size)
            food_y = random.randrange(0, height - block_size, block_size)
            if length % 5 == 0:
                speed += 1

        win.fill(blue)
        draw_grid()
        pygame.draw.rect(win, red, [food_x, food_y, block_size, block_size])
        draw_snake(snake)
        show_score(length - 1, high_score, (speed - initial_speed + 1))

        pygame.display.update()
        clock.tick(speed)

    save_high_score(length - 1)
    pygame.quit()
    quit()

# Run the game
game_loop()
