# from machine import Pin,SPI,PWM
# import framebuf
# import time
# import os

from lcd_3inch5 import LCD_3inch5

def draw_moon_horizontal(phase):

    cx = 240
    cy = 100
    r = 50

    import math

    # Kąt fazy
    angle = 2 * math.pi * phase

    # Określa położenie terminatora.
    # -1 = pełnia
    #  0 = kwadra
    # +1 = cienki sierp
    terminator = math.cos(angle)

    for y in range(cy - r, cy + r + 1):

        dy = y - cy

        # Szerokość tarczy w tym wierszu
        half_width = math.sqrt(r * r - dy * dy)

        # Położenie terminatora dla tego wiersza
        boundary = terminator * half_width

        for x in range(cx - r, cx + r + 1):

            dx = x - cx

            # Czy jesteśmy wewnątrz okrągłej tarczy?
            if dx * dx + dy * dy <= r * r:

                if phase < 0.5:

                    # Rosnący Księżyc:
                    # światło po prawej stronie
                    if dx >= boundary:
                        LCD.pixel(x, y, LCD.WHITE)

                else:

                    # Malejący Księżyc:
                    # światło po lewej stronie
                    if dx <= -boundary:
                        LCD.pixel(x, y, LCD.WHITE)


def moon_texture(x, y):
    """
    Sztuczna tekstura Księżyca.
    Zwraca jasność 0-255.
    """

    import math

    # Kilka sztucznych kraterów / mórz
    value = 210

    craters = [
        (125, 110, 12, 80),
        (180, 105, 18, 60),
        (145, 150, 25, 45),
        (190, 155, 10, 90),
        (115, 175, 16, 55),
        (170, 185, 22, 70),
        (205, 130, 8, 100),
        (135, 90, 7, 50),
    ]

    for cx, cy, radius, darkness in craters:

        dx = x - cx
        dy = y - cy

        distance = math.sqrt(dx * dx + dy * dy)

        if distance < radius:

            # Im bliżej środka krateru,
            # tym ciemniejszy
            factor = 1 - distance / radius

            value -= int(darkness * factor)

    # Ograniczenie jasności
    if value < 40:
        value = 40

    if value > 255:
        value = 255

    return value


def rgb565_gray(value):

    """
    Zamienia jasność 0-255 na kolor RGB565.
    """

    r = value >> 3
    g = value >> 2
    b = value >> 3

    return (r << 11) | (g << 5) | b


def draw_moon_part(phase, global_y_start):

    import math

    # Pozycja Księżyca
    cx = 160
    cy = 145
    radius = 140

    # Nów
    if phase <= 0.001 or phase >= 0.999:
        return

    # Terminator
    k = math.cos(2 * math.pi * phase)

    if phase >= 0.5:
        k = -k

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

        if phase < 0.5:

            start_x = int(terminator_x)

            if start_x < left:
                start_x = left

            if start_x > right:
                start_x = right

            for x in range(start_x, right + 1):

                brightness = moon_texture(
                    x,
                    global_y
                )

                color = rgb565_gray(brightness)

                LCD.pixel(x, local_y, color)

        else:

            end_x = int(terminator_x)

            if end_x < left:
                end_x = left

            if end_x > right:
                end_x = right

            for x in range(left, end_x + 1):

                brightness = moon_texture(
                    x,
                    global_y
                )

                color = rgb565_gray(brightness)

                LCD.pixel(x, local_y, color)


def draw_moon(phase):

    # Górna część ekranu

    LCD.fill(LCD.BLACK)

    draw_moon_part(
        phase,
        0
    )

    LCD.show_up()


    # Dolna część ekranu

    LCD.fill(LCD.BLACK)

    draw_moon_part(
        phase,
        240
    )

    LCD.show_down()

# ============================================
# MAIN
# ============================================

if __name__ == '__main__':

    LCD = LCD_3inch5()
    LCD.bl_ctrl(100)

    phase = 0.5

    LCD.fill(LCD.BLACK)

    LCD.text("MOON TEXTURE", 180, 20, LCD.WHITE)

    draw_moon(phase)

    while True:
        time.sleep(1)

#     phases = [
#         0.0,
#         0.1,
#         0.2,
#         0.25,
#         0.3,
#         0.4,
#         0.5,
#         0.6,
#         0.7,
#         0.75,
#         0.8,
#         0.9,
#         1.0
#     ]
# 
#     while True:
# 
#         for phase in phases:
# 
#             print("phase =", phase)
# 
#             draw_moon(phase)
# 
#             time.sleep(1)
