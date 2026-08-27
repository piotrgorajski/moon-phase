import framebuf
import math

from lcd_3inch5 import LCD_3inch5


# =========================================================
# USTAWIENIA GRAFIKI
# =========================================================

MOON_FILE = "moon.raw"

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
# JASNOŚĆ CIEMNEJ STRONY
# =========================================================

DARK_SIDE_BRIGHTNESS = 0.30


# =========================================================
# LCD
# =========================================================

LCD = LCD_3inch5()
LCD.bl_ctrl(100)


# =========================================================
# TABLICA GRAYSCALE -> RGB565
# =========================================================

# Przygotowujemy konwersję wszystkich 256 możliwych
# wartości jasności tylko raz.
#
# Każdy kolor zajmuje 2 bajty.

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

    # Kolejność wymagana przez LCD.pixel()/framebuf
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

# 300 pikseli × 2 bajty RGB565

row_buffer = bytearray(MOON_W * 2)

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
    gray_row,
    global_y,
    local_y,
    phase
):

    # -----------------------------------------------------
    # Wyczyść cały wiersz.
    #
    # Dzięki temu wszystko poza Księżycem pozostaje czarne.
    # -----------------------------------------------------

    for i in range(len(row_buffer)):
        row_buffer[i] = 0


    # -----------------------------------------------------
    # Pozycja wiersza względem środka Księżyca
    # -----------------------------------------------------

    dy = global_y - CY

    if abs(dy) > RADIUS:
        return


    # -----------------------------------------------------
    # Szerokość tarczy w tym wierszu
    # -----------------------------------------------------

    half_width = math.sqrt(
        RADIUS * RADIUS
        -
        dy * dy
    )


    left = int(CX - half_width)
    right = int(CX + half_width)


    # -----------------------------------------------------
    # Terminator
    # -----------------------------------------------------

    k = math.cos(2 * math.pi * phase)

    if phase >= 0.5:
        k = -k


    terminator_x = (
        CX
        +
        k * half_width
    )


    # -----------------------------------------------------
    # Granica jasnej części
    # -----------------------------------------------------

    if phase < 0.5:

        light_start = int(terminator_x)

        if light_start < left:
            light_start = left

        if light_start > right:
            light_start = right

    else:

        light_end = int(terminator_x)

        if light_end < left:
            light_end = left

        if light_end > right:
            light_end = right


    # =====================================================
    # BUDOWANIE WIERSZA RGB565
    # =====================================================

    for x in range(left, right + 1):

        tx = x - MOON_X

        if tx < 0 or tx >= MOON_W:
            continue


        original_gray = gray_row[tx]


        # -------------------------------------------------
        # USTALAMY JASNOŚĆ
        # -------------------------------------------------

        if phase < 0.5:

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
        # RGB565
        # -------------------------------------------------

        row_buffer[2 * (x - left)] = colors[
            2 * gray
        ]

        row_buffer[2 * (x - left) + 1] = colors[
            2 * gray + 1
        ]


    # =====================================================
    # JEDEN BLIT ZAMIAST SETEK LCD.PIXEL()
    # =====================================================

    LCD.blit(
        row_fb,
        left,
        local_y
    )


# =========================================================
# RYSOWANIE CZĘŚCI KSIĘŻYCA
# =========================================================

def draw_moon_part(
    phase,
    global_y_start,
    rows,
    f
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
            phase
        )


# =========================================================
# RYSOWANIE CAŁEGO KSIĘŻYCA
# =========================================================

def draw_moon(phase):

    if phase < 0.0:
        phase = 0.0

    if phase > 1.0:
        phase = 1.0


    # =====================================================
    # GÓRA
    # =====================================================

    f = open(MOON_FILE, "rb")

    LCD.fill(LCD.BLACK)

    draw_moon_part(
        phase,
        0,
        240,
        f
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
        f
    )

    LCD.show_down()

    f.close()