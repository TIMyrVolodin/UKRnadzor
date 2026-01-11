import pygame
import sys

# ---------------- НАЛАШТУВАННЯ ----------------
WIDTH, HEIGHT = 800, 600
FPS = 60
INTRO_HOLD_TIME = 2000

# ---------------- ІНІЦІАЛІЗАЦІЯ ----------------
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("UKRnadzor game")
clock = pygame.time.Clock()

# ---------------- ШРИФТИ ----------------
font_big = pygame.font.SysFont("arial", 48)
font_mid = pygame.font.SysFont("arial", 36)

# ---------------- МУЗИКА ----------------
def play_music(file, fade_ms=1000):
    pygame.mixer.music.fadeout(fade_ms)
    pygame.time.delay(fade_ms)
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(-1, fade_ms=fade_ms)

# ---------------- ІНТРО РЕСУРСИ ----------------
text_surface = font_big.render("Lgvp_entertaiment present", True, (255, 255, 255))
text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 120))

intro_image = pygame.image.load("intro_image.jpg").convert()
intro_image = pygame.transform.scale(intro_image, (300, 300))
intro_image_rect = intro_image.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60))

intro_sound = pygame.mixer.Sound("intro_sound.mp3")
intro_sound.set_volume(0.5)

# ---------------- ЛОБІ РЕСУРСИ ----------------
lobby_bg = pygame.image.load("lobby_bg.png").convert()
lobby_bg = pygame.transform.scale(lobby_bg, (WIDTH, HEIGHT))

# ---------------- КНОПКИ ----------------
def draw_button(rect, text):
    pygame.draw.rect(screen, (50, 50, 50), rect, border_radius=8)
    pygame.draw.rect(screen, (200, 200, 200), rect, 2, border_radius=8)
    txt = font_mid.render(text, True, (255, 255, 255))
    screen.blit(txt, txt.get_rect(center=rect.center))

start_btn = pygame.Rect(300, 240, 200, 50)
credits_btn = pygame.Rect(300, 310, 200, 50)
idea_btn = pygame.Rect(300, 380, 200, 50)
back_btn = pygame.Rect(300, 500, 200, 50)

# ---------------- ІНТРО ----------------
def intro():
    alpha = 0
    fade_in = True
    hold_start = None

    intro_sound.play()

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((0, 0, 0))

        img = intro_image.copy()
        txt = text_surface.copy()
        img.set_alpha(alpha)
        txt.set_alpha(alpha)

        screen.blit(img, intro_image_rect)
        screen.blit(txt, text_rect)

        if fade_in:
            alpha += 5
            if alpha >= 255:
                alpha = 255
                fade_in = False
                hold_start = pygame.time.get_ticks()
        else:
            if pygame.time.get_ticks() - hold_start >= INTRO_HOLD_TIME:
                alpha -= 5
                if alpha <= 0:
                    break

        pygame.display.update()

    intro_sound.stop()

# ---------------- ФАЛЬШИВА ЗАГРУЗКА ----------------
def fake_loading():
    load_time = 3000  # загальна тривалість фальшивої загрузки в мс
    bar_width = 400
    bar_height = 30
    bar_x = (WIDTH - bar_width) // 2
    bar_y = HEIGHT // 2
    start_ticks = pygame.time.get_ticks()

    # Зменшуємо гучність музики головного меню
    for i in range(50):
        vol = pygame.mixer.music.get_volume()
        pygame.mixer.music.set_volume(max(0, vol - 0.02))
        pygame.time.delay(20)  # плавне убавлення гучності

    running = True
    while running:
        clock.tick(FPS)
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        elapsed = pygame.time.get_ticks() - start_ticks
        progress = min(1, elapsed / load_time)
        percent = int(progress * 100)

        pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, int(bar_width * progress), bar_height))
        txt = font_mid.render(f"{percent}%", True, (255, 255, 255))
        screen.blit(txt, txt.get_rect(center=(WIDTH // 2, bar_y - 40)))

        pygame.display.update()

        if progress >= 1:
            running = False

    pygame.mixer.music.set_volume(0.5)

# ---------------- ОСНОВНИЙ ЦИКЛ ГРИ (1 вибір) ----------------
def main_game():
    pygame.mixer.music.stop()  # музика лобі більше не грає

    bg_image = pygame.image.load("game_bg.png").convert()
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

    char_image = pygame.image.load("character.png").convert_alpha()

    char_scale = 0.3
    char_alpha = 0
    char_y = HEIGHT + 80
    char_target_y = HEIGHT // 2 - 50
    char_speed = 4

    app_image = pygame.image.load("app_icon.png").convert_alpha()
    app_image = pygame.transform.scale(app_image, (100, 100))
    app_alpha = 0
    app_rect = app_image.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 70))

    block_btn = pygame.Rect(WIDTH // 2 - 170, HEIGHT - 120, 150, 55)
    unblock_btn = pygame.Rect(WIDTH // 2 + 20, HEIGHT - 120, 150, 55)

    btn_alpha = 0

    text_str = "Заблокувати цей додаток?"
    text_display = ""
    text_index = 0

    char_sound = pygame.mixer.Sound("char_sound.mp3")
    char_sound.set_volume(1.0)

    start_ticks = pygame.time.get_ticks()
    sound_played = False
    choice = None
    choice_ticks = 0

    running = True
    while running:
        clock.tick(FPS)
        screen.blit(bg_image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and choice is None:
                if block_btn.collidepoint(event.pos):
                    choice = "block"
                    choice_ticks = pygame.time.get_ticks()
                if unblock_btn.collidepoint(event.pos):
                    choice = "unblock"
                    choice_ticks = pygame.time.get_ticks()

        # звук через 3 сек
        if not sound_played and pygame.time.get_ticks() - start_ticks > 3000:
            char_sound.play()
            sound_played = True

        # персонаж — поява і збільшення
        if char_alpha < 255:
            char_alpha += 5
        if char_scale < 1:
            char_scale += 0.01
        if char_y > char_target_y:
            char_y -= char_speed

        char_img = pygame.transform.scale(
            char_image,
            (int(char_image.get_width() * char_scale),
             int(char_image.get_height() * char_scale))
        )
        char_img.set_alpha(char_alpha)
        char_rect = char_img.get_rect(center=(WIDTH // 2, char_y))
        screen.blit(char_img, char_rect)

        # текст з друком
        if text_index < len(text_str):
            if pygame.time.get_ticks() % 3 == 0:
                text_index += 1
            text_display = text_str[:text_index]

        text_surface = font_mid.render(text_display, True, (255, 255, 255))
        screen.blit(text_surface, text_surface.get_rect(center=(WIDTH // 2, HEIGHT - 200)))

        # іконка
        if app_alpha < 255:
            app_alpha += 5
        app_img = app_image.copy()
        app_img.set_alpha(app_alpha)
        screen.blit(app_img, app_rect)

        # кнопки fade-in
        if btn_alpha < 255 and choice is None:
            btn_alpha += 6

        if btn_alpha > 0 and choice is None:
            b1 = pygame.Surface(block_btn.size, pygame.SRCALPHA)
            b1.fill((220, 50, 50, btn_alpha))
            screen.blit(b1, block_btn.topleft)

            b2 = pygame.Surface(unblock_btn.size, pygame.SRCALPHA)
            b2.fill((50, 220, 80, btn_alpha))
            screen.blit(b2, unblock_btn.topleft)

            t1 = font_mid.render("Заблокувати", True, (255,255,255))
            t2 = font_mid.render("Розблокувати", True, (255,255,255))
            screen.blit(t1, t1.get_rect(center=block_btn.center))
            screen.blit(t2, t2.get_rect(center=unblock_btn.center))

        # після вибору
        if choice:
            btn_alpha -= 10

            if choice == "block":
                if app_alpha > 100:
                    app_alpha -= 4
            if char_y < HEIGHT + 200:
                char_y += char_speed

            if char_y >= HEIGHT + 200:
                running = False

        pygame.display.update()


# ---------------- ЛОБІ ----------------
def lobby():
    play_music("lobby_music.mp3")

    alpha = 255
    fade = True
    fade_start = pygame.time.get_ticks()

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_btn.collidepoint(event.pos):
                    fake_loading()
                    main_game()  # запускаємо сцену вибору

                if credits_btn.collidepoint(event.pos):
                    credits()
                    play_music("lobby_music.mp3")

                if idea_btn.collidepoint(event.pos):
                    game_idea()
                    play_music("lobby_music.mp3")

        screen.blit(lobby_bg, (0, 0))

        draw_button(start_btn, "Почати гру")
        draw_button(credits_btn, "Титри")
        draw_button(idea_btn, "Задумка гри")

        if fade:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(alpha)
            screen.blit(overlay, (0, 0))

            if pygame.time.get_ticks() - fade_start > 1000:
                alpha -= 5
                if alpha <= 0:
                    fade = False

        pygame.display.update()

# ---------------- ТИТРИ ----------------
def credits():
    play_music("credits_music.mp3")

    credits_text = [
        "ТИТРИ",
        "",
        "Розробник: timyrka_pro",
        "Дизайн: timyrka_pro / gemini",
        "Музика: google / zvukogram.com",
        "",
        "Дякую за гру!",
        "Чекайте подальших оновлень"
    ]

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(event.pos):
                    return

        screen.fill((0, 0, 0))

        y = 120
        for line in credits_text:
            txt = font_mid.render(line, True, (255, 255, 255))
            screen.blit(txt, txt.get_rect(center=(WIDTH // 2, y)))
            y += 40

        draw_button(back_btn, "Назад")
        pygame.display.update()

# ---------------- ЗАДУМКА ГРИ ----------------
def game_idea():
    play_music("idea_music.mp3")

    idea_text = [
        "у грі UKRnadzor ви працюєте в офісі з кібер безпеці",
        "",
        "ви працюєте самим головним органом",
        "ваші піддані вибирають додатки які можна заблокувати.",
        "але блокувати чи не чіпати додатки вирішувати вам",
        "ваші рішення впливають на кінцівку, будьте обережними",
        "бажаю гарної гри",
    ]

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(event.pos):
                    return

        screen.fill((0, 0, 0))

        y = 120
        for line in idea_text:
            txt = font_mid.render(line, True, (255, 255, 255))
            screen.blit(txt, txt.get_rect(center=(WIDTH // 2, y)))
            y += 40

        draw_button(back_btn, "Назад")
        pygame.display.update()

# ---------------- ЗАПУСК ----------------
intro()
pygame.time.delay(1000)
lobby()
