import framebuf
import math

from lcd_3inch5 import LCD_3inch5


# =========================================================
# USTAWIENIA
# =========================================================

BRIGHT_FILE = "moon_bright.raw"
DARK_FILE = "moon_dark.raw"

MOON_W = 300
MOON_H = 300

MOON_X = 10


# =========================================================
# GEOMETRIA
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
        RADIUS * RADIUS
        -
        dy * dy
    )

    row_left[y] = int(CX - half_width)
    row_right[y] = int(CX + half_width)
    row_half_width[y] = half_width


# =========================================================
# BUFOR WIERSZA
# =========================================================

row_buffer = bytearray(
    MOON_W * 2
)

row_fb = framebuf.FrameBuffer(
    row_buffer,
    MOON_W,
    1,
    framebuf.RGB565
)


# =========================================================
# RYSOWANIE JEDNEGO WIERSZA
# =========================================================

def draw_moon_row(
    bright_row,
    dark_row,
    global_y,
    local_y,
    k
):

    left = row_left[global_y]
    right = row_right[global_y]

    half_width = row_half_width[global_y]


    # -----------------------------------------------------
    # Jeżeli wiersz jest poza Księżycem
    # -----------------------------------------------------

    if right <= left:
        return


    # -----------------------------------------------------
    # Terminator
    # -----------------------------------------------------

    terminator_x = (
        CX
        +
        k * half_width
    )


    # -----------------------------------------------------
    # Kopiujemy całą ciemną teksturę
    #
    # Dzięki temu domyślnie cały Księżyc jest ciemny.
    # -----------------------------------------------------

    row_buffer[:] = dark_row


    # =====================================================
    # PRZYBYWAJĄCY
    # =====================================================

    if k <= 0:

        light_start = int(
            terminator_x
        )

        if light_start < left:
            light_start = left

        if light_start > right:
            light_start = right


        # -------------------------------------------------
        # Fragment jasny
        # -------------------------------------------------

        src_start = (
            2 * (light_start - MOON_X)
        )

        src_end = (
            2 * (right - MOON_X + 1)
        )

        dst_start = src_start
        dst_end = src_end


        if src_start < 0:
            src_start = 0
            dst_start = 0

        if src_end > MOON_W * 2:
            src_end = MOON_W * 2
            dst_end = src_end


        if src_start < src_end:

            row_buffer[
                dst_start:dst_end
            ] = bright_row[
                src_start:src_end
            ]


    # =====================================================
    # UBYWAJĄCY
    # =====================================================

    else:

        light_end = int(
            terminator_x
        )

        if light_end < left:
            light_end = left

        if light_end > right:
            light_end = right


        # -------------------------------------------------
        # Fragment jasny
        # -------------------------------------------------

        src_start = (
            2 * (left - MOON_X)
        )

        src_end = (
            2 * (light_end - MOON_X + 1)
        )

        dst_start = src_start
        dst_end = src_end


        if src_start < 0:
            src_start = 0
            dst_start = 0

        if src_end > MOON_W * 2:
            src_end = MOON_W * 2
            dst_end = src_end


        if src_start < src_end:

            row_buffer[
                dst_start:dst_end
            ] = bright_row[
                src_start:src_end
            ]


    # =====================================================
    # JEDEN BLIT
    # =====================================================

    LCD.blit(
        row_fb,
        MOON_X,
        local_y
    )


# =========================================================
# RYSOWANIE CZĘŚCI
# =========================================================

def draw_moon_part(
    phase,
    global_y_start,
    rows,
    bright_file,
    dark_file,
    k
):

    for local_y in range(rows):

        global_y = (
            global_y_start
            +
            local_y
        )


        bright_row = bright_file.read(
            MOON_W * 2
        )

        dark_row = dark_file.read(
            MOON_W * 2
        )


        if len(bright_row) != MOON_W * 2:
            raise RuntimeError(
                "moon_bright.raw ma zly rozmiar"
            )

        if len(dark_row) != MOON_W * 2:
            raise RuntimeError(
                "moon_dark.raw ma zly rozmiar"
            )


        draw_moon_row(
            bright_row,
            dark_row,
            global_y,
            local_y,
            k
        )


# =========================================================
# GŁÓWNA FUNKCJA
# =========================================================

def draw_moon(phase):

    if phase < 0.0:
        phase = 0.0

    if phase > 1.0:
        phase = 1.0


    # -----------------------------------------------------
    # TERMINATOR LICZYMY TYLKO RAZ
    # -----------------------------------------------------

    k = math.cos(
        2 * math.pi * phase
    )

    if phase >= 0.5:
        k = -k


    # =====================================================
    # GÓRNA CZĘŚĆ
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
        phase,
        0,
        240,
        bright_file,
        dark_file,
        k
    )


    LCD.show_up()


    bright_file.close()
    dark_file.close()


    # =====================================================
    # DOLNA CZĘŚĆ
    # =====================================================

    bright_file = open(
        BRIGHT_FILE,
        "rb"
    )

    dark_file = open(
        DARK_FILE,
        "rb"
    )


    bright_file.seek(
        240 * MOON_W * 2
    )

    dark_file.seek(
        240 * MOON_W * 2
    )


    LCD.fill(LCD.BLACK)


    draw_moon_part(
        phase,
        240,
        60,
        bright_file,
        dark_file,
        k
    )


    LCD.show_down()


    bright_file.close()
    dark_file.close()