import time
from lcd_3inch5 import LCD_3inch5

lcd = LCD_3inch5()
lcd.bl_ctrl(40)

print("TEST POWTARZALNOSCI")
print()
print("Dotknij LEWEGO DOLNEGO rogu 10 razy.")
print("Za kazdym razem nacisnij mniej wiecej w tym samym miejscu.")
print()


for i in range(10):

    # czekamy na dotyk
    while True:
        p = lcd.touch_get()
        if p:
            break
        time.sleep_ms(20)

    print(
        i + 1,
        ": RAW X =",
        p[0],
        " RAW Y =",
        p[1]
    )

    # czekamy aż puścisz ekran
    while lcd.touch_get():
        time.sleep_ms(20)

    time.sleep_ms(300)