import time
from moon_renderer import draw_moon
from moon_phase import moon_phase

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
            time.sleep(0.5)

# ============================================
# MAIN
# ============================================

if __name__ == '__main__':
    print("MOON PHASE TEST")
    
    YEAR = 2026
    MONTH = 8
    DAY = 29
    HOUR = 12
    MINUTE = 0
    
    phase, illumination, name = moon_phase(YEAR, MONTH, DAY, HOUR, MINUTE)
    print("ilumination = ", illumination)
    print("name = ", name)
    
    render_single_phase(phase)
    
    # render_phases_in_loop()
