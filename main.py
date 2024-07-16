import pygame
import random
from time import sleep

# Инициализация Pygame
pygame.init()

# Размеры экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Geometry Dash")

for i in range(5, 0, -1):
        screen.fill((0, 0, 0))
        f5 = pygame.font.Font(None, 36)
        text4 = f5.render("{}".format(i), 2, (255, 255, 255))
        screen.blit(text4, (WIDTH/ 2, HEIGHT / 2))
        pygame.display.update()
        sleep(0.3)

# Загрузка спрайта
sprite = pygame.image.load("sprite.png")
sprite = pygame.transform.scale(sprite, (50, 50))  # Изменение размера спрайта

# Загрузка спрайта шипов
spike_img = pygame.image.load("obj-spike.png")
spike_img = pygame.transform.scale(spike_img, (50, 50))  # Изменение размера шипов

# Загрузка спрайта блоков
block = pygame.image.load("block_1.png")
block = pygame.transform.scale(block,(50, 50)) # размер блоков

# Загрузка фона
background = pygame.image.load("fon.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Параметры спрайта
sprite_rect = sprite.get_rect()
sprite_rect.x = 100
sprite_rect.y = HEIGHT - sprite_rect.height - 10
first_jump_height = 15
second_jump_height = 20

# Параметры гравитации
gravity = 1
velocity_y = 0
jump_count = 0

# Параметры препятствий
obstacle_speed = 5
obstacles = []

# Интервал появления препятствий
obstacle_interval = random.randint(800,1500)
last_obstacle = pygame.time.get_ticks()

# Основной игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление прыжком
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and jump_count < 2:
        if jump_count == 0:
            velocity_y = -first_jump_height
        elif jump_count == 1:
            velocity_y = -second_jump_height
        jump_count += 1

    # Гравитация и прыжок
    sprite_rect.y += velocity_y
    if sprite_rect.y < HEIGHT - sprite_rect.height - 10:
        velocity_y += gravity
    else:
        sprite_rect.y = HEIGHT - sprite_rect.height - 10
        velocity_y = 0
        jump_count = 0

    # Генерация препятствий
    current_time = pygame.time.get_ticks()
    if current_time - last_obstacle > obstacle_interval:
        obstacle_x = WIDTH
        obstacle_y = random.randint(540, HEIGHT - 30 - 20)  # Adjusted for spike size
        obstacles.append((obstacle_x, obstacle_y))
        last_obstacle = current_time


    # Движение препятствий
    for i in range(len(obstacles)):
        obstacles[i] = (obstacles[i][0] - obstacle_speed, obstacles[i][1])

    # Удаление пройденных препятствий
    obstacles = [obstacle for obstacle in obstacles if obstacle[0] > -30]  # Adjusted for spike width

    # Проверка столкновений
    for obstacle in obstacles:
        if (sprite_rect.x < obstacle[0] + 30 and
            sprite_rect.x + sprite_rect.width > obstacle[0] and
            sprite_rect.y < obstacle[1] + 30 and
            sprite_rect.y + sprite_rect.height > obstacle[1]):
            running = False  # Конец игры при столкновении

    # Обновление экрана
    screen.blit(background, (0, 0))  # Отрисовка фона
    screen.blit(sprite, sprite_rect)  # Отрисовка спрайта игрока

    for obstacle in obstacles:
        screen.blit(spike_img, (obstacle[0], obstacle[1]))

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
