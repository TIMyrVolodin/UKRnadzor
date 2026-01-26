import pygame
import sys
import math
import random

# ---------------- НАЛАШТУВАННЯ ----------------
WIDTH, HEIGHT = 800, 600
FPS = 60
INTRO_HOLD_TIME = 2000

# ---------------- ГЛОБАЛЬНІ ЗМІННІ ----------------
music_volume = 0.5  # 0.0 - 1.0
player_decisions = {}  # Словник для зберігання рішень гравця
unlocked_endings = []  # Список розблокованих кінцівок

# ---------------- ІНІЦІАЛІЗАЦІЯ ----------------
pygame.init()
pygame.mixer.init()
pygame.mixer.music.set_volume(music_volume)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("UKRnadzor game")
clock = pygame.time.Clock()

# ---------------- ШРИФТИ ----------------
font_huge = pygame.font.SysFont("arial", 64)
font_big = pygame.font.SysFont("arial", 48)
font_mid = pygame.font.SysFont("arial", 36)
font_small = pygame.font.SysFont("arial", 22)
font_very_small = pygame.font.SysFont("arial", 18)

# ---------------- МУЗИКА ----------------
def play_music(file, fade_ms=1000):
    pygame.mixer.music.fadeout(fade_ms)
    pygame.time.delay(fade_ms)
    pygame.mixer.music.load(file)
    pygame.mixer.music.set_volume(music_volume)
    pygame.mixer.music.play(-1, fade_ms=fade_ms)

# ---------------- ЛОБІ РЕСУРСИ ----------------
lobby_bg = pygame.image.load("lobby_bg.png").convert()
lobby_bg = pygame.transform.scale(lobby_bg, (WIDTH, HEIGHT))

# ---------------- КНОПКИ ----------------
def draw_button(rect, text):
    pygame.draw.rect(screen, (50, 50, 50), rect, border_radius=8)
    pygame.draw.rect(screen, (200, 200, 200), rect, 2, border_radius=8)
    txt = font_mid.render(text, True, (255, 255, 255))
    screen.blit(txt, txt.get_rect(center=rect.center))

# Координати кнопок (змінені)
start_btn = pygame.Rect(300, 320, 200, 50)
settings_btn = pygame.Rect(300, 390, 200, 50)
credits_btn = pygame.Rect(300, 460, 200, 50)
idea_btn = pygame.Rect(300, 530, 200, 50)  # Задумка гри повернута
endings_btn = pygame.Rect(20, HEIGHT - 70, 200, 50)  # Кінцівки в лівому нижньому куті
back_btn = pygame.Rect(300, 500, 200, 50)

# ---------------- НАЛАШТУВАННЯ ----------------
def settings_menu():
    global music_volume

    slider_rect = pygame.Rect(200, 260, 400, 8)
    knob_rect = pygame.Rect(
        slider_rect.x + int(slider_rect.width * music_volume) - 8,
        slider_rect.y - 8,
        16,
        24
    )

    dragging = False

    while True:
        clock.tick(FPS)
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if knob_rect.collidepoint(event.pos):
                    dragging = True
                if back_btn.collidepoint(event.pos):
                    return

            if event.type == pygame.MOUSEBUTTONUP:
                dragging = False

            if event.type == pygame.MOUSEMOTION and dragging:
                x = max(slider_rect.x, min(event.pos[0], slider_rect.x + slider_rect.width))
                knob_rect.centerx = x
                music_volume = (knob_rect.centerx - slider_rect.x) / slider_rect.width
                pygame.mixer.music.set_volume(music_volume)

        # UI
        title = font_big.render("Налаштування", True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 160)))

        pygame.draw.rect(screen, (120, 120, 120), slider_rect)
        pygame.draw.rect(screen, (200, 200, 255), knob_rect)

        percent = int(music_volume * 100)
        txt = font_mid.render(f"Гучність музики: {percent}%", True, (255, 255, 255))
        screen.blit(txt, txt.get_rect(center=(WIDTH // 2, 220)))

        draw_button(back_btn, "Назад")
        pygame.display.update()

# ---------------- ІНТРО РЕСУРСИ ----------------
text_surface = font_big.render("Lgvp_entertaiment present", True, (255, 255, 255))
text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 120))

intro_image = pygame.image.load("intro_image.jpg").convert()
intro_image = pygame.transform.scale(intro_image, (300, 300))
intro_image_rect = intro_image.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60))

intro_sound = pygame.mixer.Sound("intro_sound.mp3")
intro_sound.set_volume(0.5)

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
    
    # Анімація затемнення до лобі
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.fill((0, 0, 0))
    for alpha in range(0, 255, 10):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        clock.tick(FPS)
    
    # Анімація світління лобі
    lobby_fade()

# ---------------- АНІМАЦІЯ СВІТЛІННЯ ЛОБІ ----------------
def lobby_fade():
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.fill((0, 0, 0))
    
    for alpha in range(255, -1, -10):
        clock.tick(FPS)
        screen.blit(lobby_bg, (0, 0))
        
        title1 = font_huge.render("Selection protocol", True, (255, 215, 0))
        title1_shadow = font_huge.render("Selection protocol", True, (128, 107, 0))
        title2 = font_mid.render("темна історія UKRnadzor", True, (200, 200, 200))
        
        screen.blit(title1_shadow, (WIDTH//2 - title1.get_width()//2 + 4, 94))
        screen.blit(title1, (WIDTH//2 - title1.get_width()//2, 90))
        screen.blit(title2, title2.get_rect(center=(WIDTH//2, 170)))
        
        draw_button(start_btn, "Почати гру")
        draw_button(settings_btn, "Налаштування")
        draw_button(credits_btn, "Титри")
        draw_button(idea_btn, "Задумка гри")  # Повернули
        draw_button(endings_btn, "Кінцівки")  # Додали нову кнопку
        
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()

# ---------------- ФАЛЬШИВА ЗАВАНТАЖЕННЯ ----------------
def fake_loading():
    screen.fill((0, 0, 0))
    
    loading_texts = [
        "Завантаження системи безпеки...",
        "Перевірка протоколів...",
        "Ініціалізація модуля рішень...",
        "Підготовка документів...",
        "Готово до роботи..."
    ]
    
    progress = 0
    current_text = 0
    dot_animation = 0
    
    hint_text = font_small.render("Підказка: Натисніть SPACE для пришвидшення", True, (150, 150, 150))
    
    while progress < 100:
        clock.tick(30)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    progress = 100
        
        screen.fill((0, 0, 0))
        
        dot_animation += 1
        dots = "." * ((dot_animation // 10) % 4)
        
        text = font_mid.render(loading_texts[current_text] + dots, True, (255, 255, 255))
        screen.blit(text, text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50)))
        
        bar_width = 400
        bar_height = 30
        bar_x = (WIDTH - bar_width) // 2
        bar_y = HEIGHT // 2 + 20
        
        pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height), border_radius=5)
        pygame.draw.rect(screen, (0, 150, 0), (bar_x, bar_y, int(bar_width * progress/100), bar_height), border_radius=5)
        pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height), 2, border_radius=5)
        
        percent_text = font_mid.render(f"{progress}%", True, (255, 255, 255))
        screen.blit(percent_text, percent_text.get_rect(center=(WIDTH//2, bar_y + bar_height + 20)))
        
        screen.blit(hint_text, hint_text.get_rect(center=(WIDTH//2, HEIGHT - 50)))
        
        pygame.display.update()
        
        progress += random.randint(1, 3)
        progress = min(100, progress)
        
        if progress >= 20 and current_text == 0:
            current_text = 1
        elif progress >= 40 and current_text == 1:
            current_text = 2
        elif progress >= 60 and current_text == 2:
            current_text = 3
        elif progress >= 80 and current_text == 3:
            current_text = 4
    
    for alpha in range(255, -1, -5):
        clock.tick(FPS)
        screen.fill((0, 0, 0))
        
        done_text = font_big.render("ЗАВАНТАЖЕННЯ ЗАВЕРШЕНО", True, (0, 255, 0))
        screen.blit(done_text, done_text.get_rect(center=(WIDTH//2, HEIGHT//2)))
        
        fade = pygame.Surface((WIDTH, HEIGHT))
        fade.fill((0, 0, 0))
        fade.set_alpha(alpha)
        screen.blit(fade, (0, 0))
        pygame.display.update()

# ---------------- ПРОЛОГ ----------------
def prologue():
    pygame.mixer.music.stop()

    pygame.mixer.music.load("Prolog.mp3")
    pygame.mixer.music.set_volume(music_volume)
    pygame.mixer.music.play(-1, fade_ms=1000)

    prolog_image = pygame.image.load("prolog.png").convert()
    prolog_image = pygame.transform.scale(prolog_image, (WIDTH, HEIGHT))

    skip_btn = pygame.Rect(WIDTH - 150, 20, 130, 35)

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

    box_width = WIDTH - 120
    box_height = 140
    box_rect = pygame.Rect(
        (WIDTH - box_width) // 2,
        HEIGHT - box_height - 30,
        box_width,
        box_height
    )
    
    text_area_rect = pygame.Rect(
        box_rect.left,
        box_rect.top,
        int(box_width * 0.85),
        box_height
    )
    
    buttons_area_rect = pygame.Rect(
        box_rect.left + int(box_width * 0.85),
        box_rect.top,
        int(box_width * 0.15),
        box_height
    )
    
    button_height = buttons_area_rect.height // 3
    nav_skip_back_btn = pygame.Rect(
        buttons_area_rect.left + 5,
        buttons_area_rect.top + 5,
        buttons_area_rect.width - 10,
        button_height - 10
    )
    nav_skip_forward_btn = pygame.Rect(
        buttons_area_rect.left + 5,
        buttons_area_rect.top + button_height + 5,
        buttons_area_rect.width - 10,
        button_height - 10
    )
    nav_back_dialog_btn = pygame.Rect(
        buttons_area_rect.left + 5,
        buttons_area_rect.top + 2 * button_height + 5,
        buttons_area_rect.width - 10,
        button_height - 10
    )
    
    show_hint = True
    hint_alpha = 255
    hint_blink = 0

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

        y = rect.top + 10
        for line in lines:
            txt_surface = font.render(line, True, color)
            surface.blit(txt_surface, (rect.left + 20, y))
            y += font.get_height() + 2

    def draw_nav_button(rect, symbol, active=True):
        color = (80, 80, 80, 200) if active else (40, 40, 40, 200)
        border_color = (180, 180, 180) if active else (80, 80, 80)
        
        button_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(button_surface, color, button_surface.get_rect(), border_radius=3)
        pygame.draw.rect(button_surface, border_color, button_surface.get_rect(), 1, border_radius=3)
        screen.blit(button_surface, rect.topleft)
        
        symbol_surf = font_small.render(symbol, True, (255, 255, 255))
        screen.blit(symbol_surf, symbol_surf.get_rect(center=rect.center))

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if skip_btn.collidepoint(event.pos):
                    pygame.mixer.music.fadeout(800)
                    return
                
                if nav_skip_back_btn.collidepoint(event.pos) and current_text < len(texts) - 1:
                    current_text = len(texts) - 1
                    displayed_text = texts[current_text]
                    char_index = len(displayed_text)
                    show_hint = False
                    
                elif nav_skip_forward_btn.collidepoint(event.pos) and current_text < len(texts) - 1:
                    if char_index >= len(texts[current_text]):
                        current_text += 1
                        displayed_text = ""
                        char_index = 0
                        last_char_time = pygame.time.get_ticks()
                        show_hint = False
                    else:
                        displayed_text = texts[current_text]
                        char_index = len(displayed_text)
                        show_hint = False
                        
                elif nav_back_dialog_btn.collidepoint(event.pos) and current_text > 0:
                    current_text -= 1
                    displayed_text = ""
                    char_index = 0
                    last_char_time = pygame.time.get_ticks()
                    show_hint = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                show_hint = False
                if char_index >= len(texts[current_text]):
                    if current_text < len(texts) - 1:
                        current_text += 1
                        displayed_text = ""
                        char_index = 0
                        last_char_time = pygame.time.get_ticks()
                    else:
                        fading_out = True
                else:
                    displayed_text = texts[current_text]
                    char_index = len(displayed_text)

        if fading_in:
            fade_alpha -= 8
            if fade_alpha <= 0:
                fade_alpha = 0
                fading_in = False

        if not fading_out and char_index < len(texts[current_text]):
            now = pygame.time.get_ticks()
            if now - last_char_time > typing_speed:
                displayed_text += texts[current_text][char_index]
                char_index += 1
                last_char_time = now

        screen.blit(prolog_image, (0, 0))

        text_box = pygame.Surface(box_rect.size, pygame.SRCALPHA)
        text_box.fill((0, 0, 0, 180))
        pygame.draw.rect(text_box, (255, 255, 255, 40),
                         text_box.get_rect(), 2, border_radius=12)
        screen.blit(text_box, box_rect.topleft)
        
        pygame.draw.line(screen, (255, 255, 255, 60), 
                        (text_area_rect.right, text_area_rect.top),
                        (text_area_rect.right, text_area_rect.bottom), 1)

        draw_wrapped_text(screen, displayed_text, text_area_rect, font_small, (255, 255, 255))
        
        counter_text = font_very_small.render(f"{current_text + 1}/{len(texts)}", True, (180, 180, 180))
        screen.blit(counter_text, (text_area_rect.left + 20, text_area_rect.bottom - 25))
        
        if show_hint and current_text == 0 and char_index == 0:
            hint_blink += 1
            hint_alpha = 150 + int(105 * math.sin(hint_blink * 0.1))
            hint_text = font_small.render("Наступна репліка на SPACE", True, (255, 255, 255))
            hint_text.set_alpha(hint_alpha)
            hint_rect = hint_text.get_rect(center=(WIDTH//2, box_rect.top - 30))
            
            hint_bg = pygame.Surface((hint_rect.width + 20, hint_rect.height + 10), pygame.SRCALPHA)
            hint_bg.fill((0, 0, 0, 150))
            pygame.draw.rect(hint_bg, (255, 255, 255, 50), hint_bg.get_rect(), 1, border_radius=5)
            screen.blit(hint_bg, (hint_rect.left - 10, hint_rect.top - 5))
            
            screen.blit(hint_text, hint_rect)

        draw_nav_button(nav_skip_back_btn, ">>", current_text < len(texts) - 1)
        draw_nav_button(nav_skip_forward_btn, ">", current_text < len(texts) - 1)
        draw_nav_button(nav_back_dialog_btn, "<", current_text > 0)

        pygame.draw.rect(screen, (60, 60, 60), skip_btn, border_radius=6)
        skip_txt = font_small.render("Пропустити", True, (255, 255, 255))
        screen.blit(skip_txt, skip_txt.get_rect(center=skip_btn.center))

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

    dark_office = pygame.image.load("temnuiofis.png").convert()
    dark_office = pygame.transform.scale(dark_office, (WIDTH, HEIGHT))

    bg_image = pygame.image.load("game_bg.png").convert()
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

    char_image_raw = pygame.image.load("character.png").convert_alpha()
    char_image = pygame.transform.scale(
        char_image_raw,
        (int(char_image_raw.get_width() * 1.4),
         int(char_image_raw.get_height() * 1.4))
    )
    char_flip = pygame.transform.flip(char_image, True, False)

    char_sound = pygame.mixer.Sound("char_sound.mp3")
    char_sound.set_volume(0.9)

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
            pygame.draw.rect(
                box,
                (255, 255, 255, 40),
                box.get_rect(),
                2,
                border_radius=16
            )
            screen.blit(box, box_rect.topleft)

            if name:
                name_surf = font_mid.render(name, True, (200, 200, 255))
                screen.blit(name_surf, (box_rect.left + 20, box_rect.top - 45))

            words = displayed.split(" ")
            line = ""
            y = box_rect.top + 20

            for word in words:
                test = line + word + " "
                if font_mid.size(test)[0] <= box_rect.width - 40:
                    line = test
                else:
                    screen.blit(
                        font_mid.render(line, True, (255, 255, 255)),
                        (box_rect.left + 20, y)
                    )
                    y += font_mid.get_height() + 4
                    line = word + " "

            screen.blit(
                font_mid.render(line, True, (255, 255, 255)),
                (box_rect.left + 20, y)
            )

            pygame.display.update()

    fade = pygame.Surface((WIDTH, HEIGHT))
    fade.fill((0, 0, 0))
    for a in range(0, 255, 10):
        fade.set_alpha(a)
        screen.blit(fade, (0, 0))
        pygame.display.update()
        clock.tick(FPS)

    screen.blit(dark_office, (0, 0))
    pygame.display.update()
    pygame.time.delay(1000)

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

    screen.blit(bg_image, (0, 0))
    pygame.display.update()
    pygame.time.delay(500)

    char_x = WIDTH + 120
    char_y = HEIGHT // 3
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

    gameplay_folder()

# ---------------- ГЕЙМПЛЕЙ З ПАПКОЮ ----------------
def gameplay_folder():
    global player_decisions
    
    play_music("game_bg.mp3", fade_ms=1500)
    
    try:
        office_bg = pygame.image.load("game_bg.png").convert()
        office_bg = pygame.transform.scale(office_bg, (WIDTH, HEIGHT))
    except:
        office_bg = pygame.Surface((WIDTH, HEIGHT))
        office_bg.fill((180, 190, 210))
    
    # Звуки з обмеженням для блокування
    try:
        happy_sound = pygame.mixer.Sound("happypeaple.mp3")
        happy_sound.set_volume(0.3)
        happy_sound_played = False
    except:
        happy_sound = None
        happy_sound_played = False
        
    try:
        block_sound = pygame.mixer.Sound("blockmusic.mp3")
        # Обмежуємо тривалість звуку блокування до 2 секунд
        block_sound.set_volume(0.4)
        block_sound_channel = None  # Для контролю відтворення
        block_sound_played = False
        block_sound_start_time = 0
    except:
        block_sound = None
        block_sound_played = False
    
    apps = [
        {
            "name": "YouTube",
            "description": "Відеохостинг з мільйонами користувачів. Містить потенційно небезпечні матеріали.",
            "popularity": 5,
            "respect": 20,
            "icon": "app_icon.png",
            "monologues": [
                "такк, глянемо. Що вони там нового насочіняли?",
                "назва папки: найважливіші додатки для заблокування?!",
                "звучить дуже стрьомно. Стоп що..",
                "перший додаток для блокування ютуб?! чим він їм неугодив",
                "хотя тут написано він небезпечний, хмм"
            ]
        },
        {
            "name": "TikTok",
            "description": "Платформа для коротких відео. Дуже популярний серед молоді, але може викликати залежність.",
            "popularity": 10,
            "respect": 60,
            "icon": "tiktok.png",
            "monologues": [
                "далі в нас... тікток",
                "Це ж дуже популярно серед молоді",
                "Але люд деградує від коротхих відео, щож вибрати?"
            ]
        },
        {
            "name": "Whatsapp",
            "description": "месенджер який використовується для шахрайства",
            "popularity": 55,
            "respect": 60,
            "icon": "watsap.png",
            "monologues": [
                "далі в нас... вацап",
                "моя бабуся цим користується",
                "тут написано:'месенджер який використовується для шахрайства'",
                "дуже дивно"
            ]
        },
        {
            "name": "VPN",
            "description": "ВПН, потрібно швидко заблокувати, НЕГАЙНО",
            "popularity": 20,
            "respect": 100,
            "icon": "VPN.png",
            "monologues": [
                "впн?!",
                "я не знаю що це таке"
            ]
        },
        {
            "name": "Wechat",
            "description": "китайський нац. месенджер.",
            "popularity": 80,
            "respect": 20,
            "icon": "wechat.png",
            "monologues": [
                "вічат? він мене так бісить коли треба заєреструватися",
                "а засіб входу є тільки він",
                "і нащо треба Україні китайський месенджер?"
            ]
        },
        {
            "name": "даркнет",
            "description": "НЕГАЙНЕ БЛОКУВАННЯ",
            "popularity": 100,
            "respect": 100,
            "icon": "Darknet.png",
            "monologues": [
                "даркнет це додаток для шахраїв",
                "в Україні його треба заблокувати"
            ]
        },
        {
            "name": "roblox",
            "description": "платформа для створювання ігрових проектів, в чаті ігор багато нехороших людей",
            "popularity": 10,
            "respect": 75,
            "icon": "roblox.png",
            "monologues": [
                "роблокс? опис звучить дуже страшно",
                "тай гра роблокс, це додаток який розрахований на дітей",
                "треба вирішувати"
            ]
        },
        {
            "name": "zoom",
            "description": "першокласники просять видалити цей додаток ізза онлайн уроків",
            "popularity": 80,
            "respect": 40,
            "icon": "zoom.png",
            "monologues": [
                "школярам треба вчитися",
                "нащо блокувати зум",
                "чи може поприколу заблокати?)"
            ]
        },
        {
            "name": "telegram",
            "description": "незаконний збір данних, є потреба блокування",
            "popularity": 10,
            "respect": 40,
            "icon": "telegram.png",
            "monologues": [
                "телеграм? в нас же група в телеграмі щоб приймати рішення",
                "що за фігня",
                "я щось невірю що вони робили цей список 2 ночі __"
            ]
        },
        {
            "name": "facebook",
            "description": "пощирюється терорестичний контент у чатах та коротких відео",
            "popularity": 50,
            "respect": 50,
            "icon": "facebook.png",
            "monologues": [
                "фейсбук??, я там часто сижу, і терорестичного контенту ненаблюдаю",
                "ну раз тут пишуть таке... треба подумати"
            ]
        },
        {
            "name": "instagram",
            "description": "порушення Законодавства україни",
            "popularity": 5,
            "respect": 10,
            "icon": "insta.png",
            "monologues": [
                "цікаво що там за порушення",
                "треба буде в гени спитати",
                "в інсті багато молодих людей сидять, боюсь уявити що вони скажуть якщо я заблокую додаток"
            ]
        },
        {
            "name": "spotify",
            "description": "деякі музичні креатори, додають і музику заборонені матеріали",
            "popularity": 30,
            "respect": 35,
            "icon": "spotyf.png",
            "monologues": [
                "які ще заборонені матеріали?!",
                "чому не можна заборонити деякі пісні",
                "нащо блокувати цілий додаток"
            ]
        },
        {
            "name": "viber",
            "description": "загроза скаму пожилих людей",
            "popularity": 15,
            "respect": 10,
            "icon": "viber.png",
            "monologues": [
                "оце звісно причина..."
            ]
        },
        {
            "name": "twich",
            "description": "твіч відмовило нам видаляти російський стрімерів",
            "popularity": 5,
            "respect": 10,
            "icon": "tvich.png",
            "monologues": [
                "боже що за фігня, вони позорять україну своїми листами в твіч",
                "вони хочуть контролювати весь народ",
                "а звинувачити хочуть мене, бо я приймаю остаточне рішення",
                "все.",
                "роблю передостаннє рішення і все, я йду додому"
            ]
        },
        {
            "name": "privat24",
            "description": "вимагання грошей",
            "popularity": 1,
            "respect": 10,
            "icon": "Privat24.png",
            "monologues": [
                "...",
                "ні ну це криша",
                "завтра звільняюсь"
            ]
        }
    ]
    
    current_app_index = 0
    current_app = apps[current_app_index]
    
    try:
        app_icon = pygame.image.load(current_app["icon"]).convert_alpha()
        app_icon = pygame.transform.scale(app_icon, (80, 80))
    except:
        app_icon = pygame.Surface((80, 80), pygame.SRCALPHA)
        pygame.draw.rect(app_icon, (255, 0, 0), (0, 0, 80, 80), border_radius=15)
        text = font_small.render("YT" if current_app_index == 0 else "TT", True, (255, 255, 255))
        app_icon.blit(text, text.get_rect(center=(40, 40)))
    
    monologue_texts = current_app["monologues"]
    current_monologue = 0
    displayed_monologue = ""
    char_index = 0
    typing_speed = 30
    last_char_time = pygame.time.get_ticks()
    
    help_btn = pygame.Rect(WIDTH - 120, 20, 100, 40)
    block_btn = pygame.Rect(0, 0, 180, 50)
    unblock_btn = pygame.Rect(0, 0, 180, 50)
    
    show_help = False
    hover_block = False
    hover_unblock = False
    flicker_timer = 0
    
    folder_y = HEIGHT + 200
    folder_target_y = 80
    folder_speed = 15
    folder_width = 500
    folder_height = 400
    
    dialog_box_height = 140
    dialog_box_y = HEIGHT + dialog_box_height
    dialog_box_target_y = HEIGHT - dialog_box_height - 30
    dialog_box_speed = 12
    dialog_box_visible = False
    dialog_box_finished = False
    
    buttons_y = HEIGHT + 100
    buttons_target_y = HEIGHT - 120
    buttons_visible = False
    buttons_speed = 10
    
    STATE_FOLDER_APPEARING = 0
    STATE_MONOLOGUE = 1
    STATE_CHOICE = 2
    STATE_FOLDER_HIDING = 3
    STATE_NEXT_APP = 4
    
    current_state = STATE_FOLDER_APPEARING
    
    running = True
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if help_btn.collidepoint(event.pos):
                    show_help = not show_help
                
                if current_state == STATE_CHOICE:
                    if block_btn.collidepoint(event.pos):
                        player_decisions[current_app["name"].lower()] = "block"
                        current_state = STATE_FOLDER_HIDING
                    
                    if unblock_btn.collidepoint(event.pos):
                        player_decisions[current_app["name"].lower()] = "unblock"
                        current_state = STATE_FOLDER_HIDING
            
            if event.type == pygame.KEYDOWN:
                if current_state == STATE_MONOLOGUE and event.key == pygame.K_SPACE:
                    if char_index < len(monologue_texts[current_monologue]):
                        displayed_monologue = monologue_texts[current_monologue]
                        char_index = len(displayed_monologue)
                    else:
                        if current_monologue < len(monologue_texts) - 1:
                            current_monologue += 1
                            displayed_monologue = ""
                            char_index = 0
                            last_char_time = pygame.time.get_ticks()
                        else:
                            current_state = STATE_CHOICE
                            dialog_box_visible = False
                            buttons_visible = True
            
            if event.type == pygame.MOUSEMOTION:
                hover_block = block_btn.collidepoint(event.pos)
                hover_unblock = unblock_btn.collidepoint(event.pos)
                
                if hover_unblock and happy_sound and not happy_sound_played and current_state == STATE_CHOICE:
                    happy_sound.play()
                    happy_sound_played = True
                elif not hover_unblock:
                    happy_sound_played = False
                
                # Обробка звуку блокування з обмеженням
                if hover_block and block_sound and not block_sound_played and current_state == STATE_CHOICE:
                    block_sound_channel = block_sound.play()
                    block_sound_start_time = pygame.time.get_ticks()
                    block_sound_played = True
                elif not hover_block and block_sound_played:
                    # Зупиняємо звук при виході з кнопки
                    if block_sound_channel:
                        block_sound_channel.stop()
                    block_sound_played = False
                elif hover_block and block_sound_played and block_sound_channel:
                    # Обмежуємо тривалість звуку до 2 секунд
                    if pygame.time.get_ticks() - block_sound_start_time > 2000:  # 2 секунди
                        block_sound_channel.stop()
                        block_sound_played = False  # Дозволяємо відтворити знову
        
        flicker_timer += 1
        
        screen.blit(office_bg, (0, 0))
        
        if current_state == STATE_FOLDER_APPEARING:
            if folder_y > folder_target_y:
                folder_y -= folder_speed
                if folder_y < folder_target_y:
                    folder_y = folder_target_y
            else:
                current_state = STATE_MONOLOGUE
                dialog_box_visible = True
        
        elif current_state == STATE_MONOLOGUE:
            if dialog_box_y > dialog_box_target_y:
                dialog_box_y -= dialog_box_speed
            
            if not dialog_box_finished and char_index < len(monologue_texts[current_monologue]):
                now = pygame.time.get_ticks()
                if now - last_char_time > typing_speed:
                    displayed_monologue += monologue_texts[current_monologue][char_index]
                    char_index += 1
                    last_char_time = now
        
        elif current_state == STATE_CHOICE:
            if buttons_y > buttons_target_y:
                buttons_y -= buttons_speed
        
        elif current_state == STATE_FOLDER_HIDING:
            folder_y += folder_speed
            if dialog_box_y < HEIGHT + dialog_box_height:
                dialog_box_y += dialog_box_speed
            if buttons_y < HEIGHT + 100:
                buttons_y += buttons_speed
            
            if folder_y > HEIGHT + 200:
                current_app_index += 1
                
                if current_app_index < len(apps):
                    current_state = STATE_NEXT_APP
                    current_app = apps[current_app_index]
                    
                    try:
                        app_icon = pygame.image.load(current_app["icon"]).convert_alpha()
                        app_icon = pygame.transform.scale(app_icon, (80, 80))
                    except:
                        app_icon = pygame.Surface((80, 80), pygame.SRCALPHA)
                        pygame.draw.rect(app_icon, (0, 200, 255), (0, 0, 80, 80), border_radius=15)
                        text = font_small.render("TT", True, (255, 255, 255))
                        app_icon.blit(text, text.get_rect(center=(40, 40)))
                    
                    monologue_texts = current_app["monologues"]
                    current_monologue = 0
                    displayed_monologue = ""
                    char_index = 0
                    last_char_time = pygame.time.get_ticks()
                    
                    folder_y = HEIGHT + 200
                    dialog_box_y = HEIGHT + dialog_box_height
                    buttons_y = HEIGHT + 100
                    dialog_box_visible = False
                    buttons_visible = False
                    
                    current_state = STATE_FOLDER_APPEARING
                else:
                    final_scene()
                    return
        
        elif current_state == STATE_NEXT_APP:
            pygame.time.delay(500)
            current_state = STATE_FOLDER_APPEARING
        
        folder_rect = pygame.Rect((WIDTH - folder_width) // 2, int(folder_y), folder_width, folder_height)
        pygame.draw.rect(screen, (100, 80, 50), folder_rect, border_radius=15)
        pygame.draw.rect(screen, (120, 100, 60), folder_rect, 3, border_radius=15)
        
        inner_rect = pygame.Rect(folder_rect.x + 20, folder_rect.y + 20, folder_rect.width - 40, folder_rect.height - 40)
        pygame.draw.rect(screen, (240, 230, 210), inner_rect, border_radius=10)
        pygame.draw.rect(screen, (200, 190, 170), inner_rect, 2, border_radius=10)
        
        tab_rect = pygame.Rect(folder_rect.x + 30, folder_rect.y - 15, 100, 30)
        pygame.draw.rect(screen, (150, 130, 100), tab_rect, border_radius=5)
        pygame.draw.rect(screen, (180, 160, 130), tab_rect, 2, border_radius=5)
        tab_text = font_small.render("ПАПКА", True, (255, 255, 255))
        screen.blit(tab_text, tab_text.get_rect(center=tab_rect.center))
        
        icon_rect = pygame.Rect(inner_rect.x + 30, inner_rect.y + 30, 80, 80)
        screen.blit(app_icon, icon_rect)
        
        tape_color = (200, 50, 50) if current_app_index == 0 else (0, 150, 200)
        tape_surface = pygame.Surface((100, 25), pygame.SRCALPHA)
        pygame.draw.rect(tape_surface, (*tape_color, 180), (0, 0, 100, 25), border_radius=3)
        tape_text = font_very_small.render("", True, (255, 255, 255))
        tape_text.set_alpha(200)
        tape_surface.blit(tape_text, tape_text.get_rect(center=(50, 12)))
        
        rotated_tape = pygame.transform.rotate(tape_surface, 30)
        tape_pos = (icon_rect.x + 10, icon_rect.y + 10)
        screen.blit(rotated_tape, tape_pos)
        
        app_title = font_big.render(current_app["name"], True, (30, 30, 30))
        screen.blit(app_title, (inner_rect.x + 130, inner_rect.y + 30))
        
        desc_rect = pygame.Rect(inner_rect.x + 30, inner_rect.y + 130, inner_rect.width - 60, 100)
        pygame.draw.rect(screen, (255, 255, 255), desc_rect, border_radius=8)
        pygame.draw.rect(screen, (220, 220, 220), desc_rect, 1, border_radius=8)
        
        words = current_app["description"].split(" ")
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if font_small.size(test_line)[0] <= desc_rect.width - 20:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)
        
        y = desc_rect.y + 10
        for line in lines:
            line_surface = font_small.render(line, True, (50, 50, 50))
            screen.blit(line_surface, (desc_rect.x + 10, y))
            y += font_small.get_height() + 2
        
        param_start_y = inner_rect.y + 250
        param_bar_width = 250
        param_bar_height = 20
        
        pop_bar_x = inner_rect.x + 30
        pop_bar_y = param_start_y
        
        pygame.draw.rect(screen, (200, 200, 200), (pop_bar_x, pop_bar_y, param_bar_width, param_bar_height), border_radius=5)
        pygame.draw.rect(screen, (50, 150, 50), (pop_bar_x, pop_bar_y, int(param_bar_width * current_app["popularity"]/100), param_bar_height), border_radius=5)
        
        pop_text = font_very_small.render(f"Згода народу: {current_app['popularity']}%", True, (30, 30, 30))
        pop_text_width = pop_text.get_width()
        
        if pop_bar_x + param_bar_width + pop_text_width + 10 > inner_rect.right:
            pop_text = pygame.font.SysFont("arial", 14).render(f"Згода народу: {current_app['popularity']}%", True, (30, 30, 30))
        
        screen.blit(pop_text, (pop_bar_x + param_bar_width + 5, pop_bar_y))
        
        res_bar_y = param_start_y + 35
        
        pygame.draw.rect(screen, (200, 200, 200), (pop_bar_x, res_bar_y, param_bar_width, param_bar_height), border_radius=5)
        pygame.draw.rect(screen, (50, 100, 200), (pop_bar_x, res_bar_y, int(param_bar_width * current_app["respect"]/100), param_bar_height), border_radius=5)
        
        res_text = font_very_small.render(f"Повага підлеглих: {current_app['respect']}%", True, (30, 30, 30))
        res_text_width = res_text.get_width()
        
        if pop_bar_x + param_bar_width + res_text_width + 10 > inner_rect.right:
            res_text = pygame.font.SysFont("arial", 14).render(f"Повага підлеглих: {current_app['respect']}%", True, (30, 30, 30))
        
        screen.blit(res_text, (pop_bar_x + param_bar_width + 5, res_bar_y))
        
        if dialog_box_visible and current_state == STATE_MONOLOGUE:
            dialog_box_width = WIDTH - 120
            dialog_box_rect = pygame.Rect(
                (WIDTH - dialog_box_width) // 2,
                dialog_box_y,
                dialog_box_width,
                dialog_box_height
            )
            
            dialog_box = pygame.Surface(dialog_box_rect.size, pygame.SRCALPHA)
            dialog_box.fill((0, 0, 0, 180))
            pygame.draw.rect(dialog_box, (255, 255, 255, 40), 
                           dialog_box.get_rect(), 2, border_radius=16)
            screen.blit(dialog_box, dialog_box_rect.topleft)
            
            monologue_words = displayed_monologue.split(" ")
            monologue_lines = []
            monologue_current = ""
            
            for word in monologue_words:
                test = monologue_current + word + " "
                if font_mid.size(test)[0] <= dialog_box_rect.width - 40:
                    monologue_current = test
                else:
                    monologue_lines.append(monologue_current)
                    monologue_current = word + " "
            monologue_lines.append(monologue_current)
            
            y_dialog = dialog_box_rect.top + 20
            for line in monologue_lines:
                line_render = font_mid.render(line, True, (255, 255, 255))
                screen.blit(line_render, (dialog_box_rect.left + 20, y_dialog))
                y_dialog += font_mid.get_height() + 4
            
            if char_index >= len(monologue_texts[current_monologue]):
                if current_monologue < len(monologue_texts) - 1:
                    hint_text = font_small.render("Натисніть SPACE для продовження", True, (200, 200, 200))
                else:
                    hint_text = font_small.render("Натисніть SPACE для прийняття рішення", True, (200, 200, 200))
                screen.blit(hint_text, hint_text.get_rect(center=(WIDTH//2, dialog_box_rect.bottom + 25)))
        
        if buttons_visible:
            block_btn.x = folder_rect.centerx - 200
            block_btn.y = buttons_y
            unblock_btn.x = folder_rect.centerx + 20
            unblock_btn.y = buttons_y
            
            block_color = (200, 50, 50) if not hover_block else (220, 70, 70)
            pygame.draw.rect(screen, block_color, block_btn, border_radius=8)
            pygame.draw.rect(screen, (150, 30, 30), block_btn, 2, border_radius=8)
            block_text = font_mid.render("Заблокувати", True, (255, 255, 255))
            screen.blit(block_text, block_text.get_rect(center=block_btn.center))
            
            unblock_color = (50, 180, 80) if not hover_unblock else (70, 200, 100)
            pygame.draw.rect(screen, unblock_color, unblock_btn, border_radius=8)
            pygame.draw.rect(screen, (30, 150, 60), unblock_btn, 2, border_radius=8)
            unblock_text = font_mid.render("Розблокувати", True, (255, 255, 255))
            screen.blit(unblock_text, unblock_text.get_rect(center=unblock_btn.center))
        
        help_color = (100, 100, 200) if not show_help else (150, 100, 100)
        pygame.draw.rect(screen, help_color, help_btn, border_radius=6)
        pygame.draw.rect(screen, (150, 150, 255), help_btn, 2, border_radius=6)
        help_button_text = font_small.render("Довідка", True, (255, 255, 255))
        screen.blit(help_button_text, help_button_text.get_rect(center=help_btn.center))
        
        if show_help:
            help_height = 80
            help_bg = pygame.Surface((WIDTH - 130, help_height), pygame.SRCALPHA)
            help_bg.fill((0, 0, 0, 220))
            pygame.draw.rect(help_bg, (255, 255, 255, 50), help_bg.get_rect(), 2, border_radius=15)
            screen.blit(help_bg, (10, 10))
            
            help_text_lines = [
                "у кожного додатка є свої шкали: згоди народу(чим менша цифра, тим більший",
                "ризик бунтів)та шкала поваги підлеглих, ураховуйте ці параметри при виборах."
            ]
            
            line1 = font_small.render(help_text_lines[0], True, (255, 255, 255))
            screen.blit(line1, (30, 30))
            
            line2 = font_small.render(help_text_lines[1], True, (255, 255, 255))
            screen.blit(line2, (30, 60))
        
        if hover_block and buttons_visible:
            flicker_alpha = abs(int(100 * math.sin(flicker_timer * 0.1)))
            flicker_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            flicker_surface.fill((100, 0, 0, flicker_alpha))
            screen.blit(flicker_surface, (0, 0))
            
            warning = font_small.render("УВАГА: Блокування додатка може мати наслідки!", True, (255, 100, 100))
            warning.set_alpha(150 + flicker_alpha)
            screen.blit(warning, warning.get_rect(center=(WIDTH//2, block_btn.y - 30)))
        
        if hover_unblock and buttons_visible:
            happy_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            happy_surface.fill((0, 100, 0, 20))
            screen.blit(happy_surface, (0, 0))
            
            positive_text = font_small.render("Рішення може підвищити вашу популярність серед народу!", True, (100, 255, 100))
            screen.blit(positive_text, positive_text.get_rect(center=(WIDTH//2, unblock_btn.y - 30)))
        
        pygame.display.update()

# ---------------- ПЕРЕВІРКА КІНЦІВОК ----------------
def check_endings():
    """Перевіряє умови для всіх кінцівок і повертає номер активної"""
    global player_decisions, unlocked_endings
    
    # Умова для кінцівки #4: заблоковано Roblox, інші додатки не чіпано (розблоковано)
    if "roblox" in player_decisions and player_decisions["roblox"] == "block":
        # Перевіряємо інші додатки
        other_apps_blocked = False
        for app_name, decision in player_decisions.items():
            if app_name != "roblox" and decision == "block":
                other_apps_blocked = True
                break
        
        if not other_apps_blocked:
            # Умова виконана - кінцівка #4
            if 4 not in unlocked_endings:
                unlocked_endings.append(4)
            return 4
    
    return 0  # Немає активних кінцівок

# ---------------- КІНЦІВКА #4 ----------------
def show_ending_4():
    """Показує кінцівку #4 - Roblox заблоковано, інші ні"""
    try:
        ending_bg = pygame.image.load("ending4.png").convert()
        ending_bg = pygame.transform.scale(ending_bg, (WIDTH, HEIGHT))
    except:
        ending_bg = pygame.Surface((WIDTH, HEIGHT))
        ending_bg.fill((30, 20, 40))
    
    play_music("ending4.mp3", fade_ms=1000)
    
    title_text = "КІНЦІВКА #4: СФОКУСОВАНИЙ ЦЕНЗОР"
    subtitle_text = "думаю блокування роблоксу було некращою ідеєю. \nви прокидаєтесь від запаху полум'я"
    
    FADE_IN = 0
    SHOW_CONTENT = 1
    FADE_OUT = 2
    
    current_state = FADE_IN
    alpha = 255
    content_alpha = 0
    timer = 0
    
    toggle_btn = pygame.Rect(WIDTH - 70, 20, 50, 50)
    menu_btn = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 200, 50)
    show_content = True
    
    running = True
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if toggle_btn.collidepoint(event.pos):
                    show_content = not show_content
                
                if show_content and menu_btn.collidepoint(event.pos):
                    current_state = FADE_OUT
        
        if current_state == FADE_IN:
            alpha -= 5
            if alpha <= 0:
                alpha = 0
                timer = pygame.time.get_ticks()
                current_state = SHOW_CONTENT
        
        elif current_state == SHOW_CONTENT:
            if pygame.time.get_ticks() - timer > 1000 and content_alpha < 255:
                content_alpha += 5
            
            content_alpha = min(255, content_alpha)
        
        elif current_state == FADE_OUT:
            alpha += 10
            if alpha >= 255:
                play_music("lobby_music.mp3")
                return
        
        screen.blit(ending_bg, (0, 0))
        
        if show_content:
            # Бокс для тексту
            text_box_width = min(WIDTH - 100, 700)  # Обмежуємо ширину
            text_box_height = 280  # Збільшено для тексту
            text_box_rect = pygame.Rect(
                (WIDTH - text_box_width) // 2,
                80,
                text_box_width,
                text_box_height
            )
            
            text_box = pygame.Surface((text_box_width, text_box_height), pygame.SRCALPHA)
            text_box.fill((0, 0, 0, 200))
            pygame.draw.rect(text_box, (255, 255, 255, 60), 
                           text_box.get_rect(), 2, border_radius=15)
            screen.blit(text_box, text_box_rect.topleft)
            
            # Заголовок
            title = font_big.render(title_text, True, (255, 215, 0))
            title.set_alpha(content_alpha)
            
            # Перевіряємо, чи заголовок вміщається
            if title.get_width() > text_box_rect.width - 40:
                # Якщо не вміщається, зменшуємо шрифт
                title = font_mid.render(title_text, True, (255, 215, 0))
                title.set_alpha(content_alpha)
            
            screen.blit(title, title.get_rect(center=(WIDTH//2, text_box_rect.top + 40)))
            
            # Підтекст (з переносом рядків і обмеженням ширини)
            subtitle_lines = subtitle_text.split("\n")
            max_line_width = text_box_rect.width - 40
            
            for i, line in enumerate(subtitle_lines):
                # Перевіряємо кожен рядок окремо
                line_surface = font_mid.render(line, True, (200, 200, 200))
                if line_surface.get_width() > max_line_width:
                    # Якщо рядок задовгий, розбиваємо його на слова
                    words = line.split(" ")
                    wrapped_lines = []
                    current_line = ""
                    
                    for word in words:
                        test_line = current_line + word + " "
                        test_surface = font_mid.render(test_line, True, (200, 200, 200))
                        if test_surface.get_width() <= max_line_width:
                            current_line = test_line
                        else:
                            wrapped_lines.append(current_line)
                            current_line = word + " "
                    wrapped_lines.append(current_line)
                    
                    # Відображаємо розбиті рядки
                    for j, wrapped_line in enumerate(wrapped_lines):
                        wrapped_surface = font_mid.render(wrapped_line, True, (200, 200, 200))
                        wrapped_surface.set_alpha(content_alpha)
                        screen.blit(wrapped_surface, 
                                  wrapped_surface.get_rect(center=(WIDTH//2, text_box_rect.top + 90 + (i+j) * 35)))
                else:
                    # Якщо рядок вміщається, відображаємо його як є
                    line_surface.set_alpha(content_alpha)
                    screen.blit(line_surface, line_surface.get_rect(center=(WIDTH//2, text_box_rect.top + 90 + i * 35)))
            
            # Кнопка меню
            menu_btn_surface = pygame.Surface((menu_btn.width, menu_btn.height), pygame.SRCALPHA)
            menu_color = (70, 70, 150, content_alpha)
            pygame.draw.rect(menu_btn_surface, menu_color, menu_btn_surface.get_rect(), border_radius=8)
            pygame.draw.rect(menu_btn_surface, (120, 120, 220, content_alpha), 
                           menu_btn_surface.get_rect(), 2, border_radius=8)
            screen.blit(menu_btn_surface, menu_btn.topleft)
            
            menu_text = font_mid.render("В головне меню", True, (255, 255, 255))
            menu_text.set_alpha(content_alpha)
            screen.blit(menu_text, menu_text.get_rect(center=menu_btn.center))
        
        # Кнопка приховування тексту (завжди видима)
        toggle_color = (80, 80, 80) if show_content else (120, 120, 120)
        pygame.draw.rect(screen, toggle_color, toggle_btn, border_radius=5)
        pygame.draw.rect(screen, (200, 200, 200), toggle_btn, 2, border_radius=5)
        
        # Малюємо "око" всередині кнопки
        eye_center = toggle_btn.center
        if show_content:
            # "Відкрите око"
            pygame.draw.circle(screen, (220, 220, 255), eye_center, 15)
            pygame.draw.circle(screen, (100, 100, 150), eye_center, 8)
        else:
            # "Закрите око" (лінія)
            pygame.draw.line(screen, (150, 150, 150), 
                           (eye_center[0] - 15, eye_center[1]),
                           (eye_center[0] + 15, eye_center[1]), 3)
        
        # Затемнення для переходів
        if alpha > 0:
            fade_surface = pygame.Surface((WIDTH, HEIGHT))
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(alpha)
            screen.blit(fade_surface, (0, 0))
        
        pygame.display.update()

# ---------------- ФІНАЛЬНА СЦЕНА ----------------
def final_scene():
    pygame.mixer.music.stop()
    
    try:
        final_image1 = pygame.image.load("finalfaz.png").convert()
        final_image1 = pygame.transform.scale(final_image1, (WIDTH, HEIGHT))
    except:
        final_image1 = pygame.Surface((WIDTH, HEIGHT))
        final_image1.fill((20, 20, 40))
        
    try:
        final_image2 = pygame.image.load("finalfaz2.png").convert()
        final_image2 = pygame.transform.scale(final_image2, (WIDTH, HEIGHT))
    except:
        final_image2 = pygame.Surface((WIDTH, HEIGHT))
        final_image2.fill((40, 20, 20))
    
    try:
        final_sound = pygame.mixer.Sound("papkaydar.mp3")
        final_sound.set_volume(0.5)
    except:
        final_sound = None
    
    final_texts = [
        "мені здається вони зробили це лише для галочки",
        "приват банк це повністю показав",
        "і взагалі.. Ця папка з додатками...",
        "Чи правильно я вчинив?",
        "Чи дійсно я захищав країну?",
        "Чи просто виконував чиюсь волю?",
        "Гена приніс цю папку...",
        "Він казав, що це важливо. хто ще замішан в її складанні, я знаю тільки пару людей, але є і +, я знаю що вони мені не друзі",
        "Але люди невинні що ці 'друзі' незнають що таке свобода слова",
        "Чи є вона взагалі в Україні",
        "Мої рішення вплинули на мільйони.",
        "Я блокував, дозволяв, контролював...",
        "Але хто контролював мене?",
        "Чи мав я вибір?",
        "Чи був я лише інструментом у чиїхось руках?"
    ]
    
    fade = pygame.Surface((WIDTH, HEIGHT))
    fade.fill((0, 0, 0))
    
    for alpha in range(255, -1, -5):
        clock.tick(FPS)
        screen.blit(final_image1, (0, 0))
        fade.set_alpha(alpha)
        screen.blit(fade, (0, 0))
        pygame.display.update()
    
    pygame.time.delay(1000)
    
    if final_sound:
        final_sound.play()
    
    for i in range(10):
        clock.tick(FPS)
        if i % 2 == 0:
            screen.blit(final_image1, (0, 0))
        else:
            screen.blit(final_image2, (0, 0))
        pygame.display.update()
        pygame.time.delay(100)
    
    screen.blit(final_image2, (0, 0))
    pygame.display.update()
    
    current_text = 0
    displayed_text = ""
    char_index = 0
    typing_speed = 35
    last_char_time = pygame.time.get_ticks()
    
    fade_alpha = 255
    fading_in = True
    
    box_width = WIDTH - 120
    box_height = 140
    box_rect = pygame.Rect(
        (WIDTH - box_width) // 2,
        HEIGHT - box_height - 30,
        box_width,
        box_height
    )
    
    text_area_rect = pygame.Rect(
        box_rect.left,
        box_rect.top,
        int(box_width * 0.85),
        box_height
    )
    
    buttons_area_rect = pygame.Rect(
        box_rect.left + int(box_width * 0.85),
        box_rect.top,
        int(box_width * 0.15),
        box_height
    )
    
    button_height = buttons_area_rect.height // 3
    nav_skip_back_btn = pygame.Rect(
        buttons_area_rect.left + 5,
        buttons_area_rect.top + 5,
        buttons_area_rect.width - 10,
        button_height - 10
    )
    nav_skip_forward_btn = pygame.Rect(
        buttons_area_rect.left + 5,
        buttons_area_rect.top + button_height + 5,
        buttons_area_rect.width - 10,
        button_height - 10
    )
    nav_back_dialog_btn = pygame.Rect(
        buttons_area_rect.left + 5,
        buttons_area_rect.top + 2 * button_height + 5,
        buttons_area_rect.width - 10,
        button_height - 10
    )
    
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

        y = rect.top + 10
        for line in lines:
            txt_surface = font.render(line, True, color)
            surface.blit(txt_surface, (rect.left + 20, y))
            y += font.get_height() + 2

    def draw_nav_button(rect, symbol, active=True):
        color = (80, 80, 80, 200) if active else (40, 40, 40, 200)
        border_color = (180, 180, 180) if active else (80, 80, 80)
        
        button_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(button_surface, color, button_surface.get_rect(), border_radius=3)
        pygame.draw.rect(button_surface, border_color, button_surface.get_rect(), 1, border_radius=3)
        screen.blit(button_surface, rect.topleft)
        
        symbol_surf = font_small.render(symbol, True, (255, 255, 255))
        screen.blit(symbol_surf, symbol_surf.get_rect(center=rect.center))

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if nav_skip_back_btn.collidepoint(event.pos) and current_text < len(final_texts) - 1:
                    current_text = len(final_texts) - 1
                    displayed_text = final_texts[current_text]
                    char_index = len(displayed_text)
                    
                elif nav_skip_forward_btn.collidepoint(event.pos) and current_text < len(final_texts) - 1:
                    if char_index >= len(final_texts[current_text]):
                        current_text += 1
                        displayed_text = ""
                        char_index = 0
                        last_char_time = pygame.time.get_ticks()
                    else:
                        displayed_text = final_texts[current_text]
                        char_index = len(displayed_text)
                        
                elif nav_back_dialog_btn.collidepoint(event.pos) and current_text > 0:
                    current_text -= 1
                    displayed_text = ""
                    char_index = 0
                    last_char_time = pygame.time.get_ticks()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if char_index >= len(final_texts[current_text]):
                    if current_text < len(final_texts) - 1:
                        current_text += 1
                        displayed_text = ""
                        char_index = 0
                        last_char_time = pygame.time.get_ticks()
                    else:
                        running = False
                else:
                    displayed_text = final_texts[current_text]
                    char_index = len(displayed_text)

        if fading_in:
            fade_alpha -= 8
            if fade_alpha <= 0:
                fade_alpha = 0
                fading_in = False

        if not fading_in and char_index < len(final_texts[current_text]):
            now = pygame.time.get_ticks()
            if now - last_char_time > typing_speed:
                displayed_text += final_texts[current_text][char_index]
                char_index += 1
                last_char_time = now

        screen.blit(final_image2, (0, 0))

        text_box = pygame.Surface(box_rect.size, pygame.SRCALPHA)
        text_box.fill((0, 0, 0, 180))
        pygame.draw.rect(text_box, (255, 255, 255, 40),
                         text_box.get_rect(), 2, border_radius=12)
        screen.blit(text_box, box_rect.topleft)
        
        pygame.draw.line(screen, (255, 255, 255, 60), 
                        (text_area_rect.right, text_area_rect.top),
                        (text_area_rect.right, text_area_rect.bottom), 1)

        draw_wrapped_text(screen, displayed_text, text_area_rect, font_small, (255, 255, 255))
        
        counter_text = font_very_small.render(f"{current_text + 1}/{len(final_texts)}", True, (180, 180, 180))
        screen.blit(counter_text, (text_area_rect.left + 20, text_area_rect.bottom - 25))

        draw_nav_button(nav_skip_back_btn, ">>", current_text < len(final_texts) - 1)
        draw_nav_button(nav_skip_forward_btn, ">", current_text < len(final_texts) - 1)
        draw_nav_button(nav_back_dialog_btn, "<", current_text > 0)

        if fading_in:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, fade_alpha))
            screen.blit(overlay, (0, 0))

        pygame.display.update()
    
    show_endings()

# ---------------- ФІНАЛЬНІ КІНЦІВКИ ----------------
def show_endings():
    """Показує відповідну кінцівку на основі рішень гравця"""
    ending_number = check_endings()
    
    if ending_number == 4:
        show_ending_4()
    else:
        screen.fill((0, 0, 0))
        end_text = font_huge.render("КІНЕЦЬ ГРИ", True, (255, 50, 50))
        screen.blit(end_text, end_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50)))
        
        info_text = font_mid.render("Кінцівки будуть додані в наступному оновленні", True, (200, 200, 200))
        screen.blit(info_text, info_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50)))
        
        pygame.display.update()
        pygame.time.delay(3000)
        
        play_music("lobby_music.mp3")
        return

# ---------------- ПЕРЕГЛЯД КІНЦІВОК ----------------
def view_endings():
    """Екран перегляду розблокованих кінцівок"""
    while True:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(event.pos):
                    return
        
        screen.fill((0, 0, 30))
        
        title = font_big.render("РОЗБЛОКОВАНІ КІНЦІВКИ", True, (255, 215, 0))
        screen.blit(title, title.get_rect(center=(WIDTH//2, 80)))
        
        y_pos = 180
        for i in range(1, 5):
            ending_rect = pygame.Rect(100, y_pos, WIDTH - 200, 80)
            
            if i in unlocked_endings:
                color = (50, 100, 50)
                text_color = (200, 255, 200)
                status_text = "РОЗБЛОКОВАНО"
            else:
                color = (50, 50, 50)
                text_color = (150, 150, 150)
                status_text = "ЗАБЛОКОВАНО"
            
            pygame.draw.rect(screen, color, ending_rect, border_radius=10)
            pygame.draw.rect(screen, (100, 100, 100), ending_rect, 2, border_radius=10)
            
            ending_title = font_mid.render(f"Кінцівка #{i}", True, text_color)
            screen.blit(ending_title, (ending_rect.x + 20, ending_rect.y + 15))
            
            status = font_small.render(status_text, True, text_color)
            screen.blit(status, (ending_rect.right - 150, ending_rect.y + 25))
            
            y_pos += 100
        
        info = font_small.render("Продовжуйте грати, щоб розблокувати всі кінцівки!", True, (200, 200, 255))
        screen.blit(info, info.get_rect(center=(WIDTH//2, HEIGHT - 80)))
        
        draw_button(back_btn, "Назад")
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

# ---------------- ЗАДУМКА ГРИ (оновлена) ----------------
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
        y = 140  # Зміщено трохи нижче
        
        # Використовуємо менший шрифт
        for line in idea_text:
            txt = font_small.render(line, True, (255, 255, 255))
            screen.blit(txt, txt.get_rect(center=(WIDTH // 2, y)))
            y += 35  # Зменшено відстань між рядками

        draw_button(back_btn, "Назад")
        pygame.display.update()

# ---------------- ЛОБІ ----------------
def lobby():
    global player_decisions
    play_music("lobby_music.mp3")

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_btn.collidepoint(event.pos):
                    player_decisions.clear()
                    fake_loading()
                    prologue()
                    main_game()
                    play_music("lobby_music.mp3")

                if settings_btn.collidepoint(event.pos):
                    settings_menu()
                    play_music("lobby_music.mp3")

                if credits_btn.collidepoint(event.pos):
                    credits()
                    play_music("lobby_music.mp3")

                if idea_btn.collidepoint(event.pos):
                    game_idea()
                    play_music("lobby_music.mp3")

                if endings_btn.collidepoint(event.pos):
                    view_endings()
                    play_music("lobby_music.mp3")

        screen.blit(lobby_bg, (0, 0))
        
        title1 = font_huge.render("Selection protocol", True, (255, 215, 0))
        title1_shadow = font_huge.render("Selection protocol", True, (128, 107, 0))
        title2 = font_mid.render("темна історія UKRnadzor", True, (200, 200, 200))
        
        screen.blit(title1_shadow, (WIDTH//2 - title1.get_width()//2 + 4, 94))
        screen.blit(title1, (WIDTH//2 - title1.get_width()//2, 90))
        screen.blit(title2, title2.get_rect(center=(WIDTH//2, 170)))
        
        draw_button(start_btn, "Почати гру")
        draw_button(settings_btn, "Налаштування")
        draw_button(credits_btn, "Титри")
        draw_button(idea_btn, "Задумка гри")  # Повернули
        draw_button(endings_btn, "Кінцівки")  # Додали нову кнопку

        pygame.display.update()

# ---------------- ЗАПУСК ----------------
intro()
lobby()
