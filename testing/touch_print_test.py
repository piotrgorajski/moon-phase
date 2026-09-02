import time
from lcd_3inch5 import LCD_3inch5


lcd = LCD_3inch5()
lcd.bl_ctrl(1)


def calibrate_touch(raw_x, raw_y):

    screen_x = 20 + (3698 - raw_x) * 440 / (3698 - 288)
    screen_y = 20 + (3834 - raw_y) * 280 / (3834 - 294)

    screen_x = int(screen_x)
    screen_y = int(screen_y)

    screen_x = max(0, min(479, screen_x))
    screen_y = max(0, min(319, screen_y))

    return screen_x, screen_y


lcd.fill(0)

print("SKALIBROWANY TOUCH TEST")
print("Dotykaj ekranu.")


while True:

    p = lcd.touch_get()

    if p:

        raw_x = p[0]
        raw_y = p[1]

        x, y = calibrate_touch(raw_x, raw_y)

        print(
            "RAW: X =", raw_x,
            "Y =", raw_y,
            "   SCREEN: X =", x,
            "Y =", y
        )

        # kropka w miejscu wykrytego dotyku
        lcd.fill_rect(x - 3, y - 3, 7, 7, 0xFFFF)

        time.sleep_ms(100)