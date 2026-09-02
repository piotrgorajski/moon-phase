import time
from lcd_3inch5 import LCD_3inch5
from machine import Pin, SPI


lcd = LCD_3inch5()
lcd.bl_ctrl(1)

print("TOUCH TEST")
print("Dotykaj kolejno wskazanych punktow.")


def wait_for_touch():
    while True:
        p = lcd.touch_get()

        if p:
            return p

        time.sleep_ms(20)


def wait_for_release():
    while lcd.touch_get():
        time.sleep_ms(20)


# =========================================================
# PUNKTY TESTOWE
# =========================================================

points = [
    ("LEWY GORNY", 20, 20),
    ("PRAWY GORNY", 460, 20),
    ("SRODEK", 240, 160),
    ("LEWY DOLNY", 20, 300),
    ("PRAWY DOLNY", 460, 300),
]


for name, sx, sy in points:

    lcd.fill(0)

    # krzyżyk pokazujący gdzie dotknąć
    lcd.line(sx - 10, sy, sx + 10, sy, 0xFFFF)
    lcd.line(sx, sy - 10, sx, sy + 10, 0xFFFF)

    print()
    print("--------------------------------")
    print(name)
    print("DOTKNIJ: SCREEN X =", sx, "Y =", sy)

    p = wait_for_touch()

    print("RAW: X =", p[0], "Y =", p[1])

    wait_for_release()

    time.sleep_ms(500)


print()
print("================================")
print("KALIBRACJA ZAKONCZONA")
print("================================")