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
# GRAYSCALE -> RGB565
# =========================================================

def rgb565_gray(gray):

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

    # LCD.pixel() wymaga tutaj zamiany kolejności bajtów.
    return (
        ((color & 0xFF) << 8)
        |
        (color >> 8)
    )


# =========================================================
# ODCZYT TEKSTURY
# =========================================================

def read_texture_row(f):

    row = f.read(MOON_W)

    if len(row) != MOON_W:
        raise RuntimeError(
            "moon.raw ma zly rozmiar"
        )

    return row


# =========================================================
# RYSOWANIE CZĘŚCI KSIĘŻYCA
# =========================================================

def draw_moon_part(phase, global_y_start, rows, f):

    # -----------------------------------------------------
    # TERMINATOR
    #
    # Nasza wcześniejsza, sprawdzona matematyka.
    # -----------------------------------------------------

    k = math.cos(2 * math.pi * phase)

    if phase >= 0.5:
        k = -k


    # -----------------------------------------------------
    # WIERSZE
    # -----------------------------------------------------

    for local_y in range(rows):

        global_y = global_y_start + local_y

        gray_row = read_texture_row(f)

        dy = global_y - CY

        if abs(dy) > RADIUS:
            continue


        # Szerokość tarczy w tym wierszu
        half_width = math.sqrt(
            RADIUS * RADIUS
            -
            dy * dy
        )

        left = int(CX - half_width)
        right = int(CX + half_width)


        # Zakrzywiony terminator
        terminator_x = (
            CX
            +
            k * half_width
        )


        # =================================================
        # PRZYBYWAJĄCY
        # =================================================

        if phase < 0.5:

            light_start = int(terminator_x)

            if light_start < left:
                light_start = left

            if light_start > right:
                light_start = right


            for x in range(left, right + 1):

                tx = x - MOON_X

                if tx < 0 or tx >= MOON_W:
                    continue

                original_gray = gray_row[tx]

                if x >= light_start:

                    # Oświetlona część
                    gray = original_gray

                else:

                    # Ciemna część — nadal widoczna,
                    # ale mocno przyciemniona.
                    gray = int(
                        original_gray
                        * DARK_SIDE_BRIGHTNESS
                    )

                LCD.pixel(
                    x,
                    local_y,
                    rgb565_gray(gray)
                )


        # =================================================
        # UBYWAJĄCY
        # =================================================

        else:

            light_end = int(terminator_x)

            if light_end < left:
                light_end = left

            if light_end > right:
                light_end = right


            for x in range(left, right + 1):

                tx = x - MOON_X

                if tx < 0 or tx >= MOON_W:
                    continue

                original_gray = gray_row[tx]

                if x <= light_end:

                    # Oświetlona część
                    gray = original_gray

                else:

                    # Ciemna część
                    gray = int(
                        original_gray
                        * DARK_SIDE_BRIGHTNESS
                    )

                LCD.pixel(
                    x,
                    local_y,
                    rgb565_gray(gray)
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
    # GÓRNA CZĘŚĆ
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
    # DOLNA CZĘŚĆ
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