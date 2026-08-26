import framebuf
import math
import time

from lcd_3inch5 import LCD_3inch5


# =========================================================
# USTAWIENIA
# =========================================================

MOON_FILE = "moon.raw"

MOON_W = 300
MOON_H = 300

# Przy rotate = 0 ekran logiczny ma 320 px szerokości.
# 300 px Księżyca daje po 10 px marginesu.
MOON_X = 10

# To są dokładnie parametry naszej wcześniejszej matematyki.
cx = 160
cy = 145
radius = 140


# =========================================================
# LCD
# =========================================================

LCD = LCD_3inch5()
LCD.bl_ctrl(100)


# =========================================================
# GRAYSCALE -> RGB565
# =========================================================

colors = bytearray(256 * 2)

for g in range(256):

    r = g >> 3
    gr = g >> 2
    b = g >> 3

    c = (r << 11) | (gr << 5) | b

    # MSB FIRST — to już mamy sprawdzone
    colors[2 * g] = c >> 8
    colors[2 * g + 1] = c & 0xff


# =========================================================
# RYSOWANIE CZĘŚCI KSIĘŻYCA
# =========================================================

def draw_moon_part(phase, global_y_start, raw_data):

    # -----------------------------------------------------
    # Nów
    # -----------------------------------------------------

    if phase <= 0.001 or phase >= 0.999:
        return


    # -----------------------------------------------------
    # TERMINATOR
    #
    # TO JEST DOKŁADNIE NASZA WCZEŚNIEJSZA MATEMATYKA
    # -----------------------------------------------------

    k = math.cos(2 * math.pi * phase)

    if phase >= 0.5:
        k = -k


    # -----------------------------------------------------
    # Wiersze
    # -----------------------------------------------------

    for local_y in range(240):

        global_y = global_y_start + local_y

        dy = global_y - cy

        if abs(dy) > radius:
            continue


        # Szerokość Księżyca w tym wierszu
        half_width = math.sqrt(
            radius * radius - dy * dy
        )


        left = int(cx - half_width)
        right = int(cx + half_width)


        # Zakrzywiony terminator
        terminator_x = cx + k * half_width


        # -------------------------------------------------
        # PRZYBYWAJĄCY
        # -------------------------------------------------

        if phase < 0.5:

            start_x = int(terminator_x)

            if start_x < left:
                start_x = left

            if start_x > right:
                start_x = right


            for x in range(start_x, right + 1):

                # Współrzędne tekstury 300×300
                tx = x - MOON_X
                ty = global_y

                if tx < 0 or tx >= MOON_W:
                    continue

                if ty < 0 or ty >= MOON_H:
                    continue

                gray = raw_data[
                    ty * MOON_W + tx
                ]

                color = colors[2 * gray] << 8
                color |= colors[2 * gray + 1]

                LCD.pixel(
                    x,
                    local_y,
                    color
                )


        # -------------------------------------------------
        # UBYWAJĄCY
        # -------------------------------------------------

        else:

            end_x = int(terminator_x)

            if end_x < left:
                end_x = left

            if end_x > right:
                end_x = right


            for x in range(left, end_x + 1):

                tx = x - MOON_X
                ty = global_y

                if tx < 0 or tx >= MOON_W:
                    continue

                if ty < 0 or ty >= MOON_H:
                    continue

                gray = raw_data[
                    ty * MOON_W + tx
                ]

                color = colors[2 * gray] << 8
                color |= colors[2 * gray + 1]

                LCD.pixel(
                    x,
                    local_y,
                    color
                )


# =========================================================
# RYSOWANIE CAŁEGO KSIĘŻYCA
# =========================================================

def draw_moon(phase):

    # -----------------------------------------------------
    # Wczytujemy cały RAW
    # -----------------------------------------------------

    with open(MOON_FILE, "rb") as f:

        raw_data = f.read()


    if len(raw_data) != MOON_W * MOON_H:
        raise RuntimeError(
            "moon.raw ma zly rozmiar: "
            + str(len(raw_data))
        )


    # =====================================================
    # GÓRNA POŁOWA
    # =====================================================

    LCD.fill(LCD.BLACK)

    draw_moon_part(
        phase,
        0,
        raw_data
    )

    LCD.show_up()


    # =====================================================
    # DOLNA POŁOWA
    # =====================================================

    LCD.fill(LCD.BLACK)

    draw_moon_part(
        phase,
        240,
        raw_data
    )

    LCD.show_down()


# =========================================================
# MAIN
# =========================================================

if __name__ == '__main__':

    phase = 0.5

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