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

    row_left[y] = int(
        CX - half_width
    )

    row_right[y] = int(
        CX + half_width
    )

    row_half_width[y] = half_width


# =========================================================
# RYSOWANIE JEDNEGO WIERSZA
# =========================================================

def draw_moon_row(
    bright_row,
    dark_row,
    global_y,
    local_y,
    k,
    phase
):

    left = row_left[global_y]
    right = row_right[global_y]

    half_width = row_half_width[global_y]

    if right <= left:
        return


    # -----------------------------------------------------
    # Najpierw cały wiersz jako CIEMNA tekstura.
    # -----------------------------------------------------

    start = 2 * (left - MOON_X)
    end = 2 * (right - MOON_X + 1)

    if start < 0:
        start = 0

    if end > MOON_W * 2:
        end = MOON_W * 2

    if start < end:

        row_buffer[start:end] = \
            dark_row[start:end]


    # -----------------------------------------------------
    # TERMINATOR
    #
    # To jest dokładnie nasza wcześniejsza geometria.
    # -----------------------------------------------------

    terminator_x = (
        CX + k * half_width
    )


    # =====================================================
    # FAZA PRZYBYWAJĄCA
    # 0.0 → < 0.5
    #
    # Jasna część po PRAWEJ.
    # =====================================================

    if phase < 0.5:

        start_x = int(
            terminator_x
        )

        if start_x < left:
            start_x = left

        if start_x > right:
            start_x = right


        src_start = 2 * (
            start_x - MOON_X
        )

        src_end = 2 * (
            right - MOON_X + 1
        )

        if src_start < 0:
            src_start = 0

        if src_end > MOON_W * 2:
            src_end = MOON_W * 2

        if src_start < src_end:

            row_buffer[
                src_start:src_end
            ] = bright_row[
                src_start:src_end
            ]


    # =====================================================
    # FAZA UBYWAJĄCA
    # 0.5 → 1.0
    #
    # Jasna część po LEWEJ.
    # =====================================================

    else:

        end_x = int(
            terminator_x
        )

        if end_x < left:
            end_x = left

        if end_x > right:
            end_x = right


        src_start = 2 * (
            left - MOON_X
        )

        src_end = 2 * (
            end_x - MOON_X + 1
        )

        if src_start < 0:
            src_start = 0

        if src_end > MOON_W * 2:
            src_end = MOON_W * 2

        if src_start < src_end:

            row_buffer[
                src_start:src_end
            ] = bright_row[
                src_start:src_end
            ]


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
    k,
    phase
):

    for local_y in range(rows):

        global_y = (
            global_y_start + local_y
        )

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
            k,
            phase
        )


# =========================================================
# GŁÓWNA FUNKCJA
# =========================================================

def draw_moon(phase):

    # -----------------------------------------------------
    # Ograniczenie fazy
    # -----------------------------------------------------

    if phase < 0.0:
        phase = 0.0

    if phase > 1.0:
        phase = 1.0


    # =====================================================
    # NASZA WCZEŚNIEJ SPRAWDZONA MATEMATYKA
    # =====================================================

    k = math.cos(
        2 * math.pi * phase
    )

    if phase >= 0.5:
        k = -k


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
        k,
        phase
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

    # W RAW mamy 300 wierszy.
    # Dolna połowa LCD pokazuje wiersze 240–299.

    offset = 240 * MOON_W * 2

    bright_file.seek(offset)
    dark_file.seek(offset)

    LCD.fill(LCD.BLACK)

    draw_moon_part(
        240,
        60,
        bright_file,
        dark_file,
        k,
        phase
    )

    LCD.show_down()

    bright_file.close()
    dark_file.close()