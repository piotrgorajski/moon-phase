import time
from moon_renderer import draw_moon

def render_single_phase(phase):
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

def render_phases_in_loop():
    phases = [
        0.0,
        0.1,
        0.2,
        0.25,
        0.3,
        0.4,
        0.5,
        0.6,
        0.7,
        0.75,
        0.8,
        0.9,
        1.0
    ]
        
    while True:
        for phase in phases:
            print("phase =", phase)
            draw_moon(phase)
            time.sleep(1)

# ============================================
# MAIN
# ============================================

if __name__ == '__main__':
    print("MOON PHASE TEST")
    # render_single_phase(0.8)
    render_phases_in_loop()
