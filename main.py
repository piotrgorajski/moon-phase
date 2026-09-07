import time

from moon_phase import moon_phase
from moon_renderer import draw_moon, LCD
from ui import draw_centered
from touch import get_action
from rtc import get_datetime


# =========================================================
# DATA I CZAS Z RTC
# =========================================================

(
    TODAY_YEAR,
    TODAY_MONTH,
    TODAY_DAY,
    HOUR,
    MINUTE,
    SECOND
) = get_datetime()

print(
    "RTC:",
    "%04d-%02d-%02d %02d:%02d:%02d"
    % (
        TODAY_YEAR,
        TODAY_MONTH,
        TODAY_DAY,
        HOUR,
        MINUTE,
        SECOND
    )
)


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
# NAWIGACJA
# =========================================================

def draw_left_triangle(x, y, size, color):

    center = size // 2

    for i in range(size):

        if i <= center:
            width = 2 * i + 1
        else:
            width = 2 * (size - 1 - i) + 1

        LCD.fill_rect(
            x - width + 1,
            y + i,
            width,
            1,
            color
        )


def draw_right_triangle(x, y, size, color):

    center = size // 2

    for i in range(size):

        if i <= center:
            width = 2 * i + 1
        else:
            width = 2 * (size - 1 - i) + 1

        LCD.fill_rect(
            x,
            y + i,
            width,
            1,
            color
        )


def draw_navigation():

    draw_left_triangle(
        35, 156, 22, LCD.WHITE
    )

    draw_right_triangle(
        285, 156, 22, LCD.WHITE
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

    import time
    start = time.ticks_ms()

    draw_moon(phase)

    elapsed = time.ticks_diff(time.ticks_ms(), start)
    print("Czas wykonania:", elapsed, "ms")


    # -----------------------------------------------------
    # FAZA
    # -----------------------------------------------------

    draw_centered(
        LCD,
        phase_name,
        80,
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
        105,
        LCD.WHITE
    )
    
    # -----------------------------------------------------
    # DATA / DZISIAJ
    # -----------------------------------------------------

    is_today = (
        VIEW_YEAR == TODAY_YEAR and
        VIEW_MONTH == TODAY_MONTH and
        VIEW_DAY == TODAY_DAY
    )

#     if is_today:
#         date_text = "DZISIAJ"
#     else:
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
        160,
        LCD.WHITE
    )
    
    if is_today:
        draw_centered(
            LCD,
            "(DZISIAJ)",
            180,
            LCD.WHITE
        )
    
    # -----------------------------------------------------
    # NAWIGACJA
    # -----------------------------------------------------

    draw_navigation()


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
    