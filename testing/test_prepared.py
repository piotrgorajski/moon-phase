import framebuf

from lcd_3inch5 import LCD_3inch5


MOON_W = 300
MOON_H = 300

MOON_X = 10

LCD = LCD_3inch5()
LCD.bl_ctrl(100)

f = open("moon_bright.raw", "rb")

row = bytearray(MOON_W * 2)

fb = framebuf.FrameBuffer(
    row,
    MOON_W,
    1,
    framebuf.RGB565
)

LCD.fill(LCD.BLACK)

for y in range(240):

    data = f.read(MOON_W * 2)

    if len(data) != MOON_W * 2:
        raise RuntimeError("Zly rozmiar RAW")

    row[:] = data

    LCD.blit(
        fb,
        MOON_X,
        y
    )

LCD.show_up()

f.close()


f = open("moon_bright.raw", "rb")

f.seek(240 * MOON_W * 2)

LCD.fill(LCD.BLACK)

for y in range(60):

    data = f.read(MOON_W * 2)

    if len(data) != MOON_W * 2:
        raise RuntimeError("Zly rozmiar RAW")

    row[:] = data

    LCD.blit(
        fb,
        MOON_X,
        y
    )

LCD.show_down()

f.close()

print("Gotowe")