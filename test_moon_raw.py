# test_moon_raw.py
# Testuje moon.raw na ekranie Waveshare.
#
# Zalozenie:
# - Twoj dzialajacy sterownik jest zapisany jako lcd_3inch5.py
# - w sterowniku self.rotate = 0
#
# Jezeli sterownik ma inna nazwe, zmien tylko ponizsza linie importu.

import framebuf
from lcd_3inch5 import LCD_3inch5

MOON_W = 300
MOON_H = 300
MOON_X = 10      # (320 - 300) / 2
MOON_Y = 0

LCD = LCD_3inch5()
LCD.bl_ctrl(100)

f = open("moon.raw", "rb")

# Jeden wiersz obrazu jako RGB565.
row = bytearray(MOON_W * 2)
row_fb = framebuf.FrameBuffer(row, MOON_W, 1, framebuf.RGB565)

# Tablica konwersji grayscale -> RGB565.
colors = bytearray(256 * 2)
for g in range(256):
    r = g >> 3
    gr = g >> 2
    b = g >> 3
    c = (r << 11) | (gr << 5) | b
    colors[2*g] = c & 0xff
    colors[2*g + 1] = c >> 8

# GORA ekranu: fizyczne y=0..239
LCD.fill(LCD.BLACK)

for y in range(240):
    gray = f.read(MOON_W)
    if len(gray) != MOON_W:
        raise RuntimeError("moon.raw ma zly rozmiar")

    for x in range(MOON_W):
        g = gray[x]
        row[2*x] = colors[2*g]
        row[2*x + 1] = colors[2*g + 1]

    LCD.blit(row_fb, MOON_X, y)

LCD.show_up()

# DOL ekranu: fizyczne y=240..299
LCD.fill(LCD.BLACK)

for y in range(60):
    gray = f.read(MOON_W)
    if len(gray) != MOON_W:
        raise RuntimeError("moon.raw ma zly rozmiar")

    for x in range(MOON_W):
        g = gray[x]
        row[2*x] = colors[2*g]
        row[2*x + 1] = colors[2*g + 1]

    LCD.blit(row_fb, MOON_X, y)

LCD.show_down()

f.close()

print("Gotowe - wyswietlono pelny Ksiezyc z moon.raw")
