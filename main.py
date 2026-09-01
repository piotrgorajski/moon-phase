import time

from moon_phase import moon_phase
from moon_renderer import draw_moon, LCD
from ui import draw_centered


# =========================================================
# DATA TESTOWA
# =========================================================

YEAR = 2026
MONTH = 8
DAY = 27

HOUR = 0
MINUTE = 0


# =========================================================
# FAZA KSIĘŻYCA
# =========================================================

phase, illumination, phase_name = moon_phase(
    YEAR,
    MONTH,
    DAY,
    HOUR,
    MINUTE
)


print("MOON UI TEST")
print()

print(
    "Date: %04d-%02d-%04d"
    % (YEAR, MONTH, DAY)
)

print(
    "Phase: %.4f"
    % phase
)

print(
    "Illumination: %.1f%%"
    % illumination
)

print(
    "Phase name: %s"
    % phase_name
)


# =========================================================
# KSIĘŻYC
# =========================================================

draw_moon(phase)


# =========================================================
# DOLNA CZĘŚĆ UI
# =========================================================


# ---------------------------------------------------------
# DATA
# ---------------------------------------------------------

date_text = (
    "%02d.%02d.%04d"
    % (
        DAY,
        MONTH,
        YEAR
    )
)

draw_centered(
    LCD,
    date_text,
    75,
    LCD.WHITE
)


# ---------------------------------------------------------
# FAZA
# ---------------------------------------------------------

draw_centered(
    LCD,
    phase_name,
    100,
    LCD.WHITE
)


# ---------------------------------------------------------
# OŚWIETLENIE
# ---------------------------------------------------------

illumination_text = (
    "%.1f%%"
    % illumination
)

draw_centered(
    LCD,
    illumination_text,
    125,
    LCD.WHITE
)


# =========================================================
# WYŚWIETLENIE
# =========================================================

LCD.show_down()


while True:
    time.sleep(1)