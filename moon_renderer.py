import framebuf
import math

from lcd_3inch5 import LCD_3inch5


# =========================================================
# USTAWIENIA
# =========================================================

MOON_FILE = "moon.raw"

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
# JASNOŚĆ CIEMNEJ STRONY
# =========================================================

DARK_SIDE_BRIGHTNESS = 0.30


# =========================================================
# LCD
# =========================================================

LCD = LCD_3inch5()
LCD.bl_ctrl(100)


# =========================================================
# TABLICA RGB565
# =========================================================

colors = bytearray(256 * 2)

for gray in range(256):

    r = gray >> 3
    g = gray >> 2
    b = gray >> 3

    color = (
        (r << 11)
        |
        (g << 5)
        |
        b
    )

    # Kolejność bajtów dla naszego LCD
    color = (
        ((color & 0xFF) << 8)
        |
        (color >> 8)
    )

    colors[2 * gray] = color & 0xFF
    colors[2 * gray + 1] = color >> 8


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

# Przygotowujemy geometrię Księżyca tylko raz.
#
# Dla każdego globalnego Y zapamiętujemy:
#
#   left
#   right
#   half_width
#
# Dzięki temu podczas każdego renderowania fazy
# nie musimy ponownie wykonywać sqrt().

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
# FUNKCJA RYSUJĄCA JEDEN WIERSZ
# =========================================================

def draw_moon_row(
    gray_row,
    global_y,
    local_y,
    k
):

    left = row_left[global_y]
    right = row_right[global_y]
    half_width = row_half_width[global_y]


    # Jeżeli ten wiersz nie należy do Księżyca
    if right <= left:
        return


    # =====================================================
    # TERMINATOR
    # =====================================================

    terminator_x = (
        CX
        +
        k * half_width
    )


    # =====================================================
    # GRANICA OŚWIETLONEJ CZĘŚCI
    # =====================================================

    if k <= 0:

        # Przybywający / pierwsza połowa cyklu
        light_start = int(terminator_x)

        if light_start < left:
            light_start = left

        if light_start > right:
            light_start = right

    else:

        # Ubywający / druga połowa cyklu
        light_end = int(terminator_x)

        if light_end < left:
            light_end = left

        if light_end > right:
            light_end = right


    # =====================================================
    # ZEROWANIE WIERSZA
    # =====================================================

    # Tylko obszar wykorzystany przez Księżyc.
    #
    # Poza nim ekran i tak jest czarny.

    start_i = 2 * (left - MOON_X)
    end_i = 2 * (right - MOON_X + 1)

    for i in range(start_i, end_i):
        row_buffer[i] = 0


    # =====================================================
    # GENEROWANIE PIXELI
    # =====================================================

    for x in range(left, right + 1):

        tx = x - MOON_X

        if tx < 0 or tx >= MOON_W:
            continue


        original_gray = gray_row[tx]


        # -------------------------------------------------
        # JASNA / CIEMNA STRONA
        # -------------------------------------------------

        if k <= 0:

            if x >= light_start:

                gray = original_gray

            else:

                gray = int(
                    original_gray
                    * DARK_SIDE_BRIGHTNESS
                )

        else:

            if x <= light_end:

                gray = original_gray

            else:

                gray = int(
                    original_gray
                    * DARK_SIDE_BRIGHTNESS
                )


        # -------------------------------------------------
        # GOTOWY KOLOR RGB565
        # -------------------------------------------------

        ci = gray << 1

        bi = 2 * (x - left)

        row_buffer[bi] = colors[ci]
        row_buffer[bi + 1] = colors[ci + 1]


    # =====================================================
    # JEDEN BLIT
    # =====================================================

    LCD.blit(
        row_fb,
        left,
        local_y
    )


# =========================================================
# RYSOWANIE CZĘŚCI
# =========================================================

def draw_moon_part(
    phase,
    global_y_start,
    rows,
    f,
    k
):

    for local_y in range(rows):

        global_y = global_y_start + local_y

        gray_row = f.read(MOON_W)

        if len(gray_row) != MOON_W:
            raise RuntimeError(
                "moon.raw ma zly rozmiar"
            )


        draw_moon_row(
            gray_row,
            global_y,
            local_y,
            k
        )


# =========================================================
# CAŁY KSIĘŻYC
# =========================================================

def draw_moon(phase):

    # -----------------------------------------------------
    # Ograniczenie zakresu
    # -----------------------------------------------------

    if phase < 0.0:
        phase = 0.0

    if phase > 1.0:
        phase = 1.0


    # -----------------------------------------------------
    # COS LICZYMY TYLKO RAZ
    # -----------------------------------------------------

    k = math.cos(
        2 * math.pi * phase
    )

    if phase >= 0.5:
        k = -k


    # =====================================================
    # GÓRA
    # =====================================================

    f = open(MOON_FILE, "rb")

    LCD.fill(LCD.BLACK)

    draw_moon_part(
        phase,
        0,
        240,
        f,
        k
    )

    LCD.show_up()

    f.close()


    # =====================================================
    # DÓŁ
    # =====================================================

    f = open(MOON_FILE, "rb")

    f.seek(240 * MOON_W)

    LCD.fill(LCD.BLACK)

    draw_moon_part(
        phase,
        240,
        60,
        f,
        k
    )

    LCD.show_down()

    f.close()