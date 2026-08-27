import time
from moon_renderer import draw_moon, LCD


phase = 0.5

print("TEST LCD")

LCD.fill(LCD.BLACK)

start = time.ticks_ms()

LCD.show_up()

t1 = time.ticks_ms()

LCD.show_down()

t2 = time.ticks_ms()

print("show_up:", time.ticks_diff(t1, start), "ms")
print("show_down:", time.ticks_diff(t2, t1), "ms")
print("RAZEM:", time.ticks_diff(t2, start), "ms")

while True:
    time.sleep(1)