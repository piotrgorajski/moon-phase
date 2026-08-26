import math
import time

from lcd_3inch5 import LCD_3inch5


# =========================================================
# USTAWIENIA
# =========================================================

MOON_FILE = "moon.raw"

MOON_W = 300
MOON_H = 300

# Ekran logiczny przy rotate = 0 ma 320 px szerokości.
# Obraz 300 px -> 10 px marginesu z lewej.
MOON_X = 10


# =========================================================
# GEOMETRIA PRAWDZIWEGO OBRAZU 300x300
# =========================================================

# Środek obrazu 300x300
cx = 159.5
cy = 149.5

# Promień odpowiadający praktycznie całej tarczy
radius = 149.5


# =========================================================
# LCD
# =========================================================

LCD = LCD_3inch5()
LCD.bl_ctrl(100)


# =========================================================
# GRAYSCALE -> RGB565
# =========================================================

def rgb565_gray(g):

    r = g >> 3
    gr = g >> 2
    b = g >> 3

    color = (r << 11) | (gr << 5) | b

    # framebuf RGB565 na RP2040 zapisuje kolory little-endian,
    # więc dla LCD.pixel() musimy zamienić bajty.
    return ((color & 0xFF) << 8) | (color >> 8)


# =========================================================
# RYSOWANIE CZĘŚCI KSIĘŻYCA
# =========================================================

def draw_moon_part(phase, global_y_start, rows, f):

    # -----------------------------------------------------
    # NÓW
    # -----------------------------------------------------

    if phase <= 0.001 or phase >= 0.999:

        # Nic nie rysujemy, ale musimy przejść przez
        # odpowiednią liczbę wierszy pliku.
        for _ in range(rows):
            gray = f.read(MOON_W)

            if len(gray) != MOON_W:
                raise RuntimeError(
                    "moon.raw ma zly rozmiar"
                )

        return


    # -----------------------------------------------------
    # TERMINATOR
    #
    # DOKŁADNIE TA SAMA MATEMATYKA,
    # KTÓRĄ WYPRACOWALIŚMY WCZEŚNIEJ
    # -----------------------------------------------------

    k = math.cos(2 * math.pi * phase)

    if phase >= 0.5:
        k = -k


    # -----------------------------------------------------
    # WIERSZE
    # -----------------------------------------------------

    for local_y in range(rows):

        global_y = global_y_start + local_y

        gray = f.read(MOON_W)

        if len(gray) != MOON_W:
            raise RuntimeError(
                "moon.raw ma zly rozmiar"
            )


        dy = global_y - cy

        if abs(dy) > radius:
            continue


        # Szerokość tarczy w tym wierszu
        half_width = math.sqrt(
            radius * radius - dy * dy
        )


        left = int(cx - half_width)
        right = int(cx + half_width)


        # Zakrzywiony terminator
        terminator_x = cx + k * half_width


        # -------------------------------------------------
        # PRZYBYWAJĄCY KSIĘŻYC
        # -------------------------------------------------

        if phase < 0.5:

            start_x = int(terminator_x)

            if start_x < left:
                start_x = left

            if start_x > right:
                start_x = right


            for x in range(start_x, right + 1):

                tx = x - MOON_X

                if tx < 0 or tx >= MOON_W:
                    continue

                g = gray[tx]

                # UWAGA:
                # LCD.pixel() dostaje bezpośrednio RGB565.
                color = rgb565_gray(g)

                LCD.pixel(
                    x,
                    local_y,
                    color
                )


        # -------------------------------------------------
        # UBYWAJĄCY KSIĘŻYC
        # -------------------------------------------------

        else:

            end_x = int(terminator_x)

            if end_x < left:
                end_x = left

            if end_x > right:
                end_x = right


            for x in range(left, end_x + 1):

                tx = x - MOON_X

                if tx < 0 or tx >= MOON_W:
                    continue

                g = gray[tx]

                color = rgb565_gray(g)

                LCD.pixel(
                    x,
                    local_y,
                    color
                )


# =========================================================
# CAŁY KSIĘŻYC
# =========================================================

def draw_moon(phase):

    # =====================================================
    # GÓRNA POŁOWA
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
    # DOLNA POŁOWA
    # =====================================================

    f = open(MOON_FILE, "rb")

    # Pomijamy pierwsze 240 wierszy obrazu.
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


# =========================================================
# MAIN
# =========================================================

if __name__ == '__main__':

    phase = 0.25

    print("MOON PHASE TEST")
    print("phase =", phase)

    start = time.ticks_ms()

    draw_moon(phase)

    elapsed = time.ticks_diff(
        time.ticks_ms(),
        start
    )

    print("Render:", elapsed, "ms")

    while True:
        time.sleep(1)