import time

from moon_phase import moon_phase
from moon_renderer import draw_moon, LCD


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
    "Date: %04d-%02d-%02d"
    % (
        YEAR,
        MONTH,
        DAY
    )
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
#
# Nie czyścimy ekranu!
# Dolne 60 px zawiera już Księżyc.
# =========================================================


# Data
date_text = (
    "%02d.%02d.%04d"
    % (
        DAY,
        MONTH,
        YEAR
    )
)

LCD.text(
    date_text,
    110,
    75,
    LCD.WHITE
)


# Oświetlenie
illumination_text = (
    "%.1f%%"
    % illumination
)

LCD.text(
    illumination_text,
    125,
    110,
    LCD.WHITE
)


# Nazwa fazy
LCD.text(
    phase_name,
    75,
    145,
    LCD.WHITE
)


LCD.show_down()


while True:
    time.sleep(1)