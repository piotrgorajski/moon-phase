# moon_phase.py
#
# Obliczanie fazy Księżyca.
#
# Konwencja phase:
#
#   0.00 = NÓW
#   0.25 = PIERWSZA KWADRA
#   0.50 = PEŁNIA
#   0.75 = OSTATNIA KWADRA
#   1.00 = NÓW
#
# Zwracamy:
#   phase             0.0 ... 1.0
#   illumination      0 ... 100 %
#   phase_name        nazwa fazy


import math


# Znany nów:
# 6 stycznia 2000, 18:14 UTC
NEW_MOON_JD = 2451550.25972

# Średni miesiąc synodyczny
SYNODIC_MONTH = 29.530588853


def julian_day(
    year,
    month,
    day,
    hour=0,
    minute=0
):

    """
    Oblicza Julian Day dla podanej daty i godziny UTC.
    """

    if month <= 2:
        year -= 1
        month += 12

    a = year // 100
    b = 2 - a + (a // 4)

    jd = (
        int(365.25 * (year + 4716))
        + int(30.6001 * (month + 1))
        + day
        + b
        - 1524.5
    )

    # Część doby.
    jd += (
        hour
        + minute / 60.0
    ) / 24.0

    return jd


def get_phase_name(phase):

    """
    Zwraca nazwę aktualnej fazy.
    """

    if phase < 0.0625:
        return "NOW"

    if phase < 0.1875:
        return "ROSNACY SIERP"

    if phase < 0.3125:
        return "PIERWSZA KWADRA"

    if phase < 0.4375:
        return "ROSNACY GARB"

    if phase < 0.5625:
        return "PELNIA"

    if phase < 0.6875:
        return "MALEJACY GARB"

    if phase < 0.8125:
        return "OSTATNIA KWADRA"

    if phase < 0.9375:
        return "MALEJACY SIERP"

    return "NOW"


def moon_phase(
    year,
    month,
    day,
    hour=12,
    minute=0
):

    """
    Oblicza fazę Księżyca.

    Parametry:
        year
        month
        day
        hour   - godzina UTC
        minute - minuta UTC

    Domyślnie używamy południa UTC.
    """

    jd = julian_day(
        year,
        month,
        day,
        hour,
        minute
    )

    # Ile czasu minęło od znanego nowiu?
    days = jd - NEW_MOON_JD

    # Pozycja w cyklu synodycznym.
    phase = (
        days / SYNODIC_MONTH
    ) % 1.0


    # -----------------------------------------------------
    # OŚWIETLENIE
    # -----------------------------------------------------

    illumination = (
        0.5
        * (
            1.0
            - math.cos(
                2.0
                * math.pi
                * phase
            )
        )
    )

    illumination_percent = (
        illumination * 100.0
    )


    # -----------------------------------------------------
    # NAZWA FAZY
    # -----------------------------------------------------

    phase_name = get_phase_name(
        phase
    )


    return (
        phase,
        illumination_percent,
        phase_name
    )