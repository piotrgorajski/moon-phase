import time

from lcd_3inch5 import LCD_3inch5
from obsolete.my_touch import get_action

LCD = LCD_3inch5()
LCD.bl_ctrl(30)

LCD.fill(LCD.BLACK)
LCD.text("TOUCH ACTION TEST", 10, 10, LCD.WHITE)
LCD.text("Lewo dol: PREV", 10, 40, LCD.WHITE)
LCD.text("Prawo dol: NEXT", 10, 60, LCD.WHITE)
LCD.text("Ksiezyc: TODAY", 10, 80, LCD.WHITE)

LCD.show_up()
# LCD.show_down()


last_action = None

while True:
    # get_touch(LCD)
    action = get_action(LCD)

    if action != last_action:
        if action is not None:
            print("ACTION:", action)

        last_action = action

    time.sleep_ms(100)