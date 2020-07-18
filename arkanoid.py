from oпs import path
from random import (randrange as rnd)  # модуль РАНДОМ. Для генератора диапазона случайных чисел

import pygame, sys
from pygame.locals import *
#Долганов Владислав Валерьевич
#ФИТУ 1-4А
#Учебная практика

mainClock = pygame.time.Clock()

pygame.init()
pygame.display.set_caption("game base")
snd_dir = path.join(path.dirname(__file__), "snd")


# Добавляем музыку/звуки
pygame.mixer.music.load("8-Bit Misfits - Old Town Road.mp3")
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.3)

hit_sound = pygame.mixer.Sound(path.join(snd_dir, "expl3.wav"))
pong_sound = pygame.mixer.Sound(path.join(snd_dir, "pong.wav"))

infoObject = pygame.display.Info()
WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h  # Разрешение экрана/Ширина, Высота
fps = 60  # Кол-во кадров в секундку


screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
font = pygame.font.SysFont(None, 20)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

click = False

def main_menu():

    while True:
        img_menu = pygame.image.load("formenu.jpg").convert()
        screen.blit(img_menu, (0, 0))
        # button(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 100, (0,255,170), (0,50,0), 'Game')
        draw_text("Arkanoid v 1.2", font, (255, 255, 255), screen, 20, 20)
        draw_text(
            "made by DOLGANOFF",
            pygame.font.SysFont("Kino", 30),
            (255, 255, 255),
            screen,
            WIDTH // 2 - 102,
            HEIGHT // 2 + 100,
        )
        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 - 50, 400, 100)

        global click
        if button_1.collidepoint((mx, my)):
            if click:
                # main.run()
                run()

        pygame.draw.rect(screen, (255, 0, 0), button_1)
        draw_text('ИГРАТЬ', pygame.font.SysFont(None, 35, True), (255, 255, 255), screen, WIDTH // 2 - 50, HEIGHT // 2 - 13)
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        draw_text(
            "ИГРАТЬ",
            pygame.font.SysFont(None, 35, True),
            (255, 255, 255),
            screen,
            WIDTH // 2 - 50,
            HEIGHT // 2 - 13,
        )

        pygame.display.update()
        mainClock.tick(60)


# Задаю настройки платформы для мячика
platform_w = 330  # Ширина платформы
platform_h = 35  # Высота платформы
platform_speed = 13  # Скорость
platform = pygame.Rect(
    WIDTH // 2 - platform_w // 2, HEIGHT - platform_h - 10, platform_w, platform_h
)
# Создадим Шарик
ball_rad = 20
ball_speed = 6
ball_rect = int(ball_rad * 2 ** 0.5)
ball = pygame.Rect(rnd(ball_rect, WIDTH - ball_rect), HEIGHT // 2, ball_rect, ball_rect)
dx, dy = 1, -1

# Настройки блоков
countBlockInRow = WIDTH // 120

block_set = [
    pygame.Rect(10 + 120 * i, 40 + 70 * j, 100, 50) for i in range(countBlockInRow) for j in range(6)
]
color_set = [
    (rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(countBlockInRow) for j in range(6)
]

img = pygame.image.load("backdoor.jpg").convert()

def detect_colsn(dx, dy, ball, rect):
    if dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if dy > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top

    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy
    elif delta_x < delta_y:
        dx = -dx
    return dx, dy

def run():
    global ball
    ball = pygame.Rect(rnd(ball_rect, WIDTH - ball_rect), HEIGHT // 2, ball_rect, ball_rect)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        screen.blit(img, (0, 0))
        # Отобразим Блоки
        [
            pygame.draw.rect(screen, color_set[color], block)
            for color, block in enumerate(block_set)
        ]  # Генератор рандомных цветов
        # Отобразим платформу
        pygame.draw.rect(screen, pygame.Color("red"), platform)
        # Отобразим Шарик
        pygame.draw.circle(screen, pygame.Color("green"), ball.center, ball_rad)
        # Движение
        global dx, dy

        ball.x += ball_speed * dx
        ball.y += ball_speed * dy
        # Отражение Шарика слева
        if ball.centerx < ball_rad or ball.centerx > WIDTH - ball_rad:
            dx = -dx
        # Отражение шаркиа по середине
        if ball.centery < ball_rad:
            dy = -dy
        # Сталкновение шарика и платформы
        if (
            ball.colliderect(platform) and dy > 0
        ):  # Возвращает истинное или ложное значенеи
            dx, dy = detect_colsn(dx, dy, ball, platform)
            pong_sound.set_volume(0.1)  # громкость
            pong_sound.play()
        # Сталкновение шарика с блоками
        hit = ball.collidelist(block_set)
        if hit != -1:
            hit_rect = block_set.pop(hit)  # Удаление блока после столкновения
            hit_color = color_set.pop(hit)  # Удаление цвета блока после столкновения
            dx, dy = detect_colsn(dx, dy, ball, hit_rect)
            hit_sound.set_volume(0.1)  # громкость
            hit_sound.play()

            # Анимация удара
            hit_rect.inflate_ip(ball.width // 3, ball.height // 3)
            pygame.draw.rect(screen, hit_color, hit_rect)
            global fps
            fps += 3  # Увеличиваем кол-во кадров после уничтожения каждого блока

        # Победа/Проигрыш
        if ball.bottom > HEIGHT:
            print("GAME OVER")
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.load("looser.mp3")
            pygame.mixer.music.play(loops=-1)
            ending((250, 250, 250), False)
        elif not len(block_set):
            print("YOU WIN ")
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.load("winner.mp3")
            pygame.mixer.music.play(loops=-1)
            ending((250, 250, 250), True)

        # Пишем управление
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and platform.left > 0:
            platform.left -= platform_speed
        if key[pygame.K_RIGHT] and platform.right < WIDTH:
            platform.right += platform_speed
        # Обновление экрана
        pygame.display.flip()
        mainClock.tick(fps)

def button (x, y, w, h, bg_color, focus_bg_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if (x+w > mouse[0] > x) and (y+h > mouse[1] > y):
        pygame.draw.rect(screen, bg_color, (x, y, w, h))
        # pygame.mouse.set_cursor(cursors[0])
        if (click[0] == 1 and action != None):
            if (action == "Game"):
                run()
            elif  (action == "Exit"):
                sys.exit()
                pygame.quit()

    else:
        pygame.draw.rect(screen, focus_bg_color, (x, y, w, h))
     

def ending(bg_color, is_win):
    running = True
    while running:
        screen.fill((0, 0, 0))

		#Создание кнопок "Выйти из игры" и "ПРОДОЛЖИТЬ"
        button(WIDTH // 2 - 165, HEIGHT // 2 - 5, 400, 100, (0,255,0), (255,255,255), 'Game')
        draw_text(
            "ПРОДОЛЖИТЬ",
            pygame.font.SysFont(None, 49, True),
            (0, 0, 0),
            screen,
            WIDTH // 2 - 112,
            HEIGHT // 2 - 1,
        )
        
        button(WIDTH - 100, 50, 200, 100, (255,0,0), (255,255,255), 'Exit')
      

        text = "YOU WIN" if is_win else "YOU LOOSE"
        draw_text(
            text,
            pygame.font.SysFont(None, 60, True),
            bg_color,
            screen,
            WIDTH // 2 - 110,
            HEIGHT // 2 - 40,
        )
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                exit()
        pygame.display.update()
        mainClock.tick(60)


if __name__ == '__main__':
    main_menu()
