import pygame
import sys
import math
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
            alpha = min(255, alpha)
            if alpha == 255:
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
    load_time = 3000
    bar_width = 400
    bar_height = 30
    bar_x = (WIDTH - bar_width) // 2
    bar_y = HEIGHT // 2
    start_ticks = pygame.time.get_ticks()

    for _ in range(50):
        vol = pygame.mixer.music.get_volume()
        pygame.mixer.music.set_volume(max(0, vol - 0.02))
        pygame.time.delay(20)

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

# ---------------- ПРОЛОГ ----------------
# ---------------- ПРОЛОГ (MUSIC + WORD WRAP FIX) ----------------
def prologue():
    # ⛔ стопаємо музику лоббі
    pygame.mixer.music.stop()

    # 🎵 музика прологу
    pygame.mixer.music.load("Prolog.mp3")
    pygame.mixer.music.set_volume(0.6)
    pygame.mixer.music.play(-1, fade_ms=1000)

    prolog_image = pygame.image.load("prolog.png").convert()
    prolog_image = pygame.transform.scale(prolog_image, (WIDTH, HEIGHT))

    texts = [
        "я не думаю що приношу людям радість",
        "з іншої сторони, я завів друзів..",
        "чи хороших?.. вони просто приносять папки, а вечором просто прощаються",
        "ЯЖ БОСС, вони повинні зі мною дружити, але чи хочуть вони цього?",
        "чому мене не питають чого я хочу...",
        "...",
        "я хочу спокійного життя, а також ЩОБ ЦЕЙ СНІГ РОЗТАЯВ",
        "**дивлюсь у вікно**",
        "люди собі спокійно ходять по вулиці, а я тут сторчу і чекаю гену",
        "Чи як його там звати... о, звук у двері, гена!",
        "Час починати."
    ]

    current_text = 0
    displayed_text = ""
    char_index = 0

    typing_speed = 35
    last_char_time = pygame.time.get_ticks()

    fade_alpha = 255
    fading_in = True
    fading_out = False

    # ---- текстовий бокс ----
    box_width = WIDTH - 120
    box_height = 140
    box_rect = pygame.Rect(
        (WIDTH - box_width) // 2,
        HEIGHT - box_height - 30,
        box_width,
        box_height
    )

    # ---- функція переносу тексту ----
    def draw_wrapped_text(surface, text, rect, font, color):
        words = text.split(" ")
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= rect.width - 40:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)

        y = rect.top + 20
        for line in lines:
            txt_surface = font.render(line, True, color)
            surface.blit(txt_surface, (rect.left + 20, y))
            y += font.get_height() + 4

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if char_index >= len(texts[current_text]):
                    if current_text < len(texts) - 1:
                        current_text += 1
                        displayed_text = ""
                        char_index = 0
                        last_char_time = pygame.time.get_ticks()
                    else:
                        fading_out = True

        # fade in
        if fading_in:
            fade_alpha -= 8
            if fade_alpha <= 0:
                fade_alpha = 0
                fading_in = False

        # typing effect
        if not fading_out and char_index < len(texts[current_text]):
            now = pygame.time.get_ticks()
            if now - last_char_time > typing_speed:
                displayed_text += texts[current_text][char_index]
                char_index += 1
                last_char_time = now

        # фон
        screen.blit(prolog_image, (0, 0))

        # текстовий бокс
        text_box = pygame.Surface(box_rect.size, pygame.SRCALPHA)
        text_box.fill((0, 0, 0, 180))
        pygame.draw.rect(
            text_box,
            (255, 255, 255, 40),
            text_box.get_rect(),
            2,
            border_radius=16
        )
        screen.blit(text_box, box_rect.topleft)

        # текст з переносом
        draw_wrapped_text(
            screen,
            displayed_text,
            box_rect,
            font_mid,
            (255, 255, 255)
        )

        # fade overlay
        if fading_in or fading_out:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, fade_alpha))
            screen.blit(overlay, (0, 0))

        if fading_out:
            fade_alpha += 10
            if fade_alpha >= 255:
                pygame.mixer.music.fadeout(1000)
                running = False

        pygame.display.update()

# ---------------- ОСНОВНИЙ ЦИКЛ ГРИ ----------------
def main_game():
    pygame.mixer.music.stop()

    # ---------- ресурси ----------
    dark_office = pygame.image.load("temnuiofis.png").convert()
    dark_office = pygame.transform.scale(dark_office, (WIDTH, HEIGHT))

    bg_image = pygame.image.load("game_bg.png").convert()
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

    char_image = pygame.image.load("character.png").convert_alpha()
    char_flip = pygame.transform.flip(char_image, True, False)

    char_sound = pygame.mixer.Sound("char_sound.mp3")
    char_sound.set_volume(0.9)

    # ---------- анімований діалог ----------
    def animated_dialog(text, name=None, bg=None, char_img=None, char_pos=None):
        box_width = WIDTH - 120
        box_height = 140

        start_y = HEIGHT + box_height
        target_y = HEIGHT - box_height - 30
        box_y = start_y

        displayed = ""
        char_index = 0
        typing_speed = 30
        last_char = pygame.time.get_ticks()

        finished_typing = False

        while True:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if not finished_typing:
                        displayed = text
                        finished_typing = True
                    else:
                        return

            if bg:
                screen.blit(bg, (0, 0))
            if char_img and char_pos:
                screen.blit(char_img, char_pos)

            if box_y > target_y:
                box_y -= 12

            if not finished_typing and box_y <= target_y:
                now = pygame.time.get_ticks()
                if now - last_char > typing_speed:
                    if char_index < len(text):
                        displayed += text[char_index]
                        char_index += 1
                        last_char = now
                    else:
                        finished_typing = True

            box_rect = pygame.Rect(
                (WIDTH - box_width) // 2,
                box_y,
                box_width,
                box_height
            )

            box = pygame.Surface(box_rect.size, pygame.SRCALPHA)
            box.fill((0, 0, 0, 180))
            pygame.draw.rect(box, (255, 255, 255, 40), box.get_rect(), 2, border_radius=16)
            screen.blit(box, box_rect.topleft)

            if name:
                name_surf = font_mid.render(name, True, (200, 200, 255))
                screen.blit(name_surf, (box_rect.left + 20, box_rect.top - 28))

            words = displayed.split(" ")
            line = ""
            y = box_rect.top + 20

            for word in words:
                test = line + word + " "
                if font_mid.size(test)[0] <= box_rect.width - 40:
                    line = test
                else:
                    screen.blit(font_mid.render(line, True, (255, 255, 255)),
                                (box_rect.left + 20, y))
                    y += font_mid.get_height() + 4
                    line = word + " "

            screen.blit(font_mid.render(line, True, (255, 255, 255)),
                        (box_rect.left + 20, y))

            pygame.display.update()

    # ---------- затемнення ----------
    fade = pygame.Surface((WIDTH, HEIGHT))
    fade.fill((0, 0, 0))
    for a in range(0, 255, 10):
        screen.blit(fade, (0, 0))
        fade.set_alpha(a)
        pygame.display.update()
        clock.tick(FPS)

    # ---------- темний офіс ----------
    screen.blit(dark_office, (0, 0))
    pygame.display.update()
    pygame.time.delay(1000)

    # ---------- діалог Гени + звук ----------
    char_sound.play()

    animated_dialog(
        "е блін, олександрович, включить світло",
        name="Гена",
        bg=dark_office
    )

    animated_dialog(
        "я включу світло оке?",
        name="Гена",
        bg=dark_office
    )

    # ---------- світлий офіс ----------
    screen.blit(bg_image, (0, 0))
    pygame.display.update()
    pygame.time.delay(500)

    # ---------- вхід персонажа ----------
    char_x = WIDTH + 120
    char_y = HEIGHT // 2 + 20
    target_x = WIDTH // 2 - 50
    walk_phase = 0

    while char_x > target_x:
        clock.tick(FPS)
        screen.blit(bg_image, (0, 0))

        walk_phase += 0.15
        offset_y = int(8 * math.sin(walk_phase))

        char_x -= 4
        screen.blit(char_image, (char_x, char_y + offset_y))
        pygame.display.update()

    # ---------- фінальний діалог ----------
    animated_dialog(
        "от він і прийшов, надіюсь багато запитань небуде ставити як завжди",
        bg=bg_image,
        char_img=char_image,
        char_pos=(char_x, char_y)
    )

    animated_dialog(
        "короче, папку сюди кладу, цей список робили 2 безсонних ночі, ну короче, чао какао",
        name="Гена",
        bg=bg_image,
        char_img=char_image,
        char_pos=(char_x, char_y)
    )

    # ---------- вихід Гени (більший і далі) ----------
    scale = 1.3
    big_char = pygame.transform.scale(
        char_flip,
        (int(char_flip.get_width() * scale),
         int(char_flip.get_height() * scale))
    )

    target_x = WIDTH + 300
    while char_x < target_x:
        clock.tick(FPS)
        screen.blit(bg_image, (0, 0))

        walk_phase += 0.15
        offset_y = int(10 * math.sin(walk_phase))

        char_x += 5
        screen.blit(big_char, (char_x, char_y + offset_y))
        pygame.display.update()

    # ---------- вибір ----------
    choice = None
    block_btn = pygame.Rect(WIDTH // 2 - 170, HEIGHT - 120, 150, 55)
    unblock_btn = pygame.Rect(WIDTH // 2 + 20, HEIGHT - 120, 150, 55)

    while choice is None:
        clock.tick(FPS)
        screen.blit(bg_image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if block_btn.collidepoint(event.pos):
                    choice = "block"
                if unblock_btn.collidepoint(event.pos):
                    choice = "unblock"

        pygame.draw.rect(screen, (200, 50, 50), block_btn, border_radius=8)
        pygame.draw.rect(screen, (50, 200, 80), unblock_btn, border_radius=8)

        screen.blit(font_mid.render("Заблокувати", True, (255,255,255)),
                    font_mid.render("Заблокувати", True, (255,255,255)).get_rect(center=block_btn.center))
        screen.blit(font_mid.render("Розблокувати", True, (255,255,255)),
                    font_mid.render("Розблокувати", True, (255,255,255)).get_rect(center=unblock_btn.center))

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
                    prologue()        # запуск прологу
                    main_game()       # після прологу геймплей

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
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, alpha))
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
