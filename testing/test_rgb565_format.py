import framebuf
from lcd_3inch5 import LCD_3inch5


LCD = LCD_3inch5()
LCD.bl_ctrl(100)

W = 320
H = 480


# =========================================================
# TEST 1 — kolory przez framebuf, tak jak w działającym
# rendererze
# =========================================================

LCD.fill(LCD.BLACK)


# Jeden wiersz 320 pikseli
row = bytearray(W * 2)

fb = framebuf.FrameBuffer(
    row,
    W,
    1,
    framebuf.RGB565
)


# =========================================================
# Funkcja zapisująca kolor RGB565
# =========================================================

def put_color(x, color):

    row[2*x] = color & 0xff
    row[2*x + 1] = color >> 8


# Standardowe kolory RGB565
BLACK  = 0x0000
WHITE  = 0xFFFF
RED    = 0xF800
GREEN  = 0x07E0
BLUE   = 0x001F
YELLOW = 0xFFE0
CYAN   = 0x07FF
MAGENTA = 0xF81F


colors = [
    BLACK,
    WHITE,
    RED,
    GREEN,
    BLUE,
    YELLOW,
    CYAN,
    MAGENTA
]


# =========================================================
# Każdy kolor jako pionowy pas
# =========================================================

stripe_width = W // len(colors)

for y in range(200):

    for i in range(len(colors)):

        color = colors[i]

        start_x = i * stripe_width
        end_x = (
            (i + 1) * stripe_width
            if i < len(colors) - 1
            else W
        )

        for x in range(start_x, end_x):

            put_color(x, color)

    LCD.blit(
        fb,
        0,
        y
    )


# =========================================================
# Drugi test — odwrotna kolejność bajtów
# =========================================================

for y in range(200, 400):

    for i in range(len(colors)):

        color = colors[i]

        start_x = i * stripe_width
        end_x = (
            (i + 1) * stripe_width
            if i < len(colors) - 1
            else W
        )

        # Tym razem ODWRACAMY kolejność bajtów.
        low = color & 0xff
        high = color >> 8

        for x in range(start_x, end_x):

            row[2*x] = high
            row[2*x + 1] = low

    LCD.blit(
        fb,
        0,
        y
    )


# =========================================================
# Pokaż obie części
# =========================================================

LCD.show_up()


# Dolna część nie jest nam teraz potrzebna.
LCD.fill(LCD.BLACK)
LCD.show_down()


print("TEST RGB565 GOTOWY")
print()
print("GORA = normalna kolejnosc bajtow")
print("DOL = odwrocona kolejnosc bajtow")