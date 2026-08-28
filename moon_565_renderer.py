import framebuf
import math

from lcd_3inch5 import LCD_3inch5


# =========================================================
# USTAWIENIA
# =========================================================

BRIGHT_FILE = "moon_bright565.raw"
DARK_FILE = "moon_dark565.raw"

MOON_W = 300
MOON_H = 300

MOON_X = 10

# =========================================================
# GEOMETRIA KSIĘŻYCA
# =========================================================

CX = 160.0
CY = 149.5
RADIUS = 149.5


# =========================================================
# LCD
# =========================================================

LCD = LCD_3inch5()
LCD.bl_ctrl(100)


# =========================================================
# BUFOR JEDNEGO WIERSZA
# =========================================================

row_buffer = bytearray(MOON_W * 2)

row_fb = framebuf.FrameBuffer(
    row_buffer,
    MOON_W,
    1,
    framebuf.RGB565
)


# =========================================================
# GEOMETRIA WIERSZY
# Liczymy tylko raz przy uruchomieniu.
# =========================================================

row_left = [0] * MOON_H
row_right = [0] * MOON_H
row_half_width = [0.0] * MOON_H

for y in range(MOON_H):

    dy = y - CY

    if abs(dy) > RADIUS:
        continue

    half_width = math.sqrt(
        RADIUS * RADIUS - dy * dy
    )

    row_left[y] = int(CX - half_width)
    row_right[y] = int(CX + half_width)
    row_half_width[y] = half_width


# =========================================================
# RYSOWANIE JEDNEGO WIERSZA
# =========================================================

def draw_moon_row(
    bright_row,
    dark_row,
    global_y,
    local_y,
    terminator
):

    left = row_left[global_y]
    right = row_right[global_y]
    half_width = row_half_width[global_y]

    if right <= left:
        return


    # -----------------------------------------------------
    # Najpierw cały Księżyc jako ciemny.
    # -----------------------------------------------------

    start = 2 * (left - MOON_X)
    end = 2 * (right - MOON_X + 1)

    if start < 0:
        start = 0

    if end > MOON_W * 2:
        end = MOON_W * 2

    if start < end:
        row_buffer[start:end] = dark_row[start:end]


    # -----------------------------------------------------
    # Terminator.
    #
    # terminator jest względną pozycją:
    #
    # -1.0 = lewa krawędź
    #  0.0 = środek
    # +1.0 = prawa krawędź
    # -----------------------------------------------------

    terminator_x = (
        CX + terminator * half_width
    )


    # =====================================================
    # FAZA PRZYBYWAJĄCA
    # 0.0 → 0.5
    #
    # Jasna część jest po PRAWEJ.
    # =====================================================

    if terminator <= 0.0:

        light_start = int(terminator_x)

        if light_start < left:
            light_start = left

        if light_start > right:
            light_start = right

        src_start = 2 * (light_start - MOON_X)
        src_end = 2 * (right - MOON_X + 1)

        if src_start < 0:
            src_start = 0

        if src_end > MOON_W * 2:
            src_end = MOON_W * 2

        if src_start < src_end:
            row_buffer[src_start:src_end] = \
                bright_row[src_start:src_end]


    # =====================================================
    # FAZA UBYWAJĄCA
    # 0.5 → 1.0
    #
    # Jasna część jest po LEWEJ.
    # =====================================================

    else:

        light_end = int(terminator_x)

        if light_end < left:
            light_end = left

        if light_end > right:
            light_end = right

        src_start = 2 * (left - MOON_X)
        src_end = 2 * (light_end - MOON_X + 1)

        if src_start < 0:
            src_start = 0

        if src_end > MOON_W * 2:
            src_end = MOON_W * 2

        if src_start < src_end:
            row_buffer[src_start:src_end] = \
                bright_row[src_start:src_end]


    # -----------------------------------------------------
    # Gotowy wiersz → LCD
    # -----------------------------------------------------

    LCD.blit(
        row_fb,
        MOON_X,
        local_y
    )


# =========================================================
# CZĘŚĆ KSIĘŻYCA
# =========================================================

def draw_moon_part(
    global_y_start,
    rows,
    bright_file,
    dark_file,
    terminator
):

    for local_y in range(rows):

        global_y = global_y_start + local_y

        bright_row = bright_file.read(
            MOON_W * 2
        )

        dark_row = dark_file.read(
            MOON_W * 2
        )

        if len(bright_row) != MOON_W * 2:
            raise RuntimeError(
                "moon_bright565.raw ma zly rozmiar"
            )

        if len(dark_row) != MOON_W * 2:
            raise RuntimeError(
                "moon_dark565.raw ma zly rozmiar"
            )

        draw_moon_row(
            bright_row,
            dark_row,
            global_y,
            local_y,
            terminator
        )


# =========================================================
# GŁÓWNA FUNKCJA
# =========================================================

def draw_moon(phase):

    # -----------------------------------------------------
    # Ograniczenie fazy do 0.0–1.0
    # -----------------------------------------------------

    if phase < 0.0:
        phase = 0.0

    if phase > 1.0:
        phase = 1.0


    # -----------------------------------------------------
    # MAPOWANIE FAZY NA POZYCJĘ TERMINATORA
    #
    # 0.00 → -1.0  NÓW
    # 0.25 →  0.0  KWADRA
    # 0.50 → +1.0  PEŁNIA
    # 0.75 →  0.0  KWADRA
    # 1.00 → -1.0  NÓW
    #
    # To jest okresowa funkcja cosinus.
    # -----------------------------------------------------

    terminator = -math.cos(
        2.0 * math.pi * phase
    )


    # =====================================================
    # GÓRA
    # =====================================================

    bright_file = open(
        BRIGHT_FILE,
        "rb"
    )

    dark_file = open(
        DARK_FILE,
        "rb"
    )

    LCD.fill(LCD.BLACK)

    draw_moon_part(
        0,
        240,
        bright_file,
        dark_file,
        terminator
    )

    LCD.show_up()

    bright_file.close()
    dark_file.close()


    # =====================================================
    # DÓŁ
    # =====================================================

    bright_file = open(
        BRIGHT_FILE,
        "rb"
    )

    dark_file = open(
        DARK_FILE,
        "rb"
    )

    # Przeskakujemy do wiersza 240.
    offset = 240 * MOON_W * 2

    bright_file.seek(offset)
    dark_file.seek(offset)

    LCD.fill(LCD.BLACK)

    draw_moon_part(
        240,
        60,
        bright_file,
        dark_file,
        terminator
    )

    LCD.show_down()

    bright_file.close()
    dark_file.close()