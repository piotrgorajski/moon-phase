import time

from moon_phase import moon_phase
from moon_renderer import draw_moon, LCD
from ui import draw_centered
from touch import get_action


# =========================================================
# DZISIEJSZA DATA - NA RAZIE TESTOWA
# =========================================================

TODAY_YEAR = 2026
TODAY_MONTH = 8
TODAY_DAY = 27

HOUR = 0
MINUTE = 0


# =========================================================
# AKTUALNIE OGLĄDANA DATA
# =========================================================

VIEW_YEAR = TODAY_YEAR
VIEW_MONTH = TODAY_MONTH
VIEW_DAY = TODAY_DAY


# =========================================================
# ZMIANA DATY
# =========================================================

def change_day(year, month, day, delta):

    timestamp = time.mktime(
        (
            year,
            month,
            day,
            12,
            0,
            0,
            0,
            0
        )
    )

    timestamp += delta * 86400

    new_date = time.localtime(timestamp)

    return (
        new_date[0],
        new_date[1],
        new_date[2]
    )


# =========================================================
# RYSOWANIE EKRANU
# =========================================================

def draw_screen():

    global VIEW_YEAR
    global VIEW_MONTH
    global VIEW_DAY

    # -----------------------------------------------------
    # FAZA KSIĘŻYCA
    # -----------------------------------------------------

    phase, illumination, phase_name = moon_phase(
        VIEW_YEAR,
        VIEW_MONTH,
        VIEW_DAY,
        HOUR,
        MINUTE
    )


    # -----------------------------------------------------
    # DEBUG
    # -----------------------------------------------------

    print()
    print("DATE: %04d-%02d-%02d" %
          (
              VIEW_YEAR,
              VIEW_MONTH,
              VIEW_DAY
          ))

    print("Phase: %.4f" % phase)
    print("Illumination: %.1f%%" % illumination)
    print("Phase name: %s" % phase_name)


    # -----------------------------------------------------
    # KSIĘŻYC
    # -----------------------------------------------------

    draw_moon(phase)


    # -----------------------------------------------------
    # DATA
    # -----------------------------------------------------

    date_text = (
        "%02d.%02d.%04d"
        % (
            VIEW_DAY,
            VIEW_MONTH,
            VIEW_YEAR
        )
    )

    draw_centered(
        LCD,
        date_text,
        75,
        LCD.WHITE
    )


    # -----------------------------------------------------
    # FAZA
    # -----------------------------------------------------

    draw_centered(
        LCD,
        phase_name,
        100,
        LCD.WHITE
    )


    # -----------------------------------------------------
    # OŚWIETLENIE
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # WYŚWIETLENIE
    # -----------------------------------------------------

    LCD.show_down()


# =========================================================
# START
# =========================================================

print("MOON UI")

draw_screen()


# =========================================================
# PĘTLA DOTYKU
# =========================================================

last_action = None

while True:

    action = get_action(LCD)

    # -----------------------------------------------------
    # Nowa akcja tylko po puszczeniu poprzedniego dotyku
    # -----------------------------------------------------

    if action is None:
        last_action = None

    elif action != last_action:

        print("ACTION:", action)

        # -------------------------------------------------
        # POPRZEDNI DZIEŃ
        # -------------------------------------------------

        if action == "PREVIOUS_DAY":

            (
                VIEW_YEAR,
                VIEW_MONTH,
                VIEW_DAY
            ) = change_day(
                VIEW_YEAR,
                VIEW_MONTH,
                VIEW_DAY,
                -1
            )

            draw_screen()


        # -------------------------------------------------
        # NASTĘPNY DZIEŃ
        # -------------------------------------------------

        elif action == "NEXT_DAY":

            (
                VIEW_YEAR,
                VIEW_MONTH,
                VIEW_DAY
            ) = change_day(
                VIEW_YEAR,
                VIEW_MONTH,
                VIEW_DAY,
                +1
            )

            draw_screen()


        # -------------------------------------------------
        # DZISIAJ
        # -------------------------------------------------

        elif action == "TODAY":

            VIEW_YEAR = TODAY_YEAR
            VIEW_MONTH = TODAY_MONTH
            VIEW_DAY = TODAY_DAY

            draw_screen()


        last_action = action

    time.sleep_ms(50)
    