# moon_phase.py

import math

PI = math.pi

# Polska / CEST w naszym obecnym projekcie
UTC_OFFSET = 2

# Now w dniu 2000-01-06 18:14 UTC
NEW_MOON_JD = 2451550.25972

# Średni miesiąc synodyczny
SYNODIC_MONTH = 29.530588853


# =========================================================
# NARZĘDZIA
# =========================================================

def deg_to_rad(x):
    return x * PI / 180.0


def julian_day(
    year,
    month,
    day,
    hour=0,
    minute=0
):

    if month <= 2:
        year -= 1
        month += 12

    A = year // 100
    B = 2 - A + A // 4

    jd = (
        int(365.25 * (year + 4716))
        + int(30.6001 * (month + 1))
        + day
        + B
        - 1524.5
    )

    jd += (
        hour
        + minute / 60.0
    ) / 24.0

    return jd


# =========================================================
# MEEUS – MOMENT GŁÓWNEJ FAZY
# =========================================================

def phase_jd(k):

    T = k / 1236.85

    jde = (
        2451550.09766
        + 29.530588861 * k
        + 0.00015437 * T * T
        - 0.000000150 * T * T * T
        + 0.00000000073 * T * T * T * T
    )

    E = (
        1.0
        - 0.002516 * T
        - 0.0000074 * T * T
    )

    M = deg_to_rad(
        2.5534
        + 29.10535670 * k
        - 0.0000014 * T * T
        - 0.00000011 * T * T * T
    )

    Mp = deg_to_rad(
        201.5643
        + 385.81693528 * k
        + 0.0107582 * T * T
        + 0.00001238 * T * T * T
        - 0.000000058 * T * T * T * T
    )

    F = deg_to_rad(
        160.7108
        + 390.67050284 * k
        - 0.0016118 * T * T
        - 0.00000227 * T * T * T
        + 0.000000011 * T * T * T * T
    )

    O = deg_to_rad(
        124.7746
        - 1.56375580 * k
        + 0.0020672 * T * T
        + 0.00000215 * T * T * T
    )

    # -----------------------------------------------------
    # Czy to nów / pełnia / kwadra?
    # -----------------------------------------------------

    phase = k % 1.0

    # Główna korekta
    if phase < 0.001 or abs(phase - 0.5) < 0.001:

        corr = (
            -0.40720 * math.sin(Mp)
            + 0.17241 * E * math.sin(M)
            + 0.01608 * math.sin(2 * Mp)
            + 0.01039 * math.sin(2 * F)
            + 0.00739 * E * math.sin(Mp - M)
            - 0.00514 * E * math.sin(Mp + M)
            + 0.00208 * E * E * math.sin(2 * M)
            - 0.00111 * math.sin(Mp - 2 * F)
            - 0.00057 * math.sin(Mp + 2 * F)
            + 0.00056 * E * math.sin(2 * Mp + M)
            - 0.00042 * math.sin(3 * Mp)
            + 0.00042 * E * math.sin(M + 2 * F)
            + 0.00038 * E * math.sin(M - 2 * F)
            - 0.00024 * E * math.sin(2 * Mp - M)
            - 0.00017 * math.sin(O)
            - 0.00007 * math.sin(Mp + 2 * M)
            + 0.00004 * math.sin(2 * Mp - 2 * F)
            + 0.00004 * math.sin(3 * M)
            + 0.00003 * math.sin(Mp + M - 2 * F)
            + 0.00003 * math.sin(2 * Mp + 2 * F)
            - 0.00003 * math.sin(Mp + M + 2 * F)
            + 0.00003 * math.sin(Mp - M + 2 * F)
            - 0.00002 * math.sin(Mp - M - 2 * F)
            - 0.00002 * math.sin(3 * Mp + M)
            + 0.00002 * math.sin(4 * Mp)
        )

    else:

        # -------------------------------------------------
        # KWADRA
        # -------------------------------------------------

        W = (
            0.00306
            - 0.00038 * E * math.cos(M)
            + 0.00026 * math.cos(Mp)
            - 0.00002 * math.cos(Mp - M)
            + 0.00002 * math.cos(Mp + M)
            + 0.00002 * math.cos(2 * F)
        )

        corr = W

    # -----------------------------------------------------
    # Dodatkowe poprawki
    # -----------------------------------------------------

    A1 = deg_to_rad(
        299.77 + 0.107408 * k - 0.000325 * T * T
    )

    A2 = deg_to_rad(
        251.88 + 0.016321 * k
    )

    A3 = deg_to_rad(
        251.83 + 26.651886 * k
    )

    A4 = deg_to_rad(
        349.42 + 36.412478 * k
    )

    A5 = deg_to_rad(
        84.66 + 18.206239 * k
    )

    A6 = deg_to_rad(
        141.74 + 53.303771 * k
    )

    A7 = deg_to_rad(
        207.14 + 2.453732 * k
    )

    A8 = deg_to_rad(
        154.84 + 7.306860 * k
    )

    A9 = deg_to_rad(
        34.52 + 27.261239 * k
    )

    A10 = deg_to_rad(
        207.19 + 0.121824 * k
    )

    A11 = deg_to_rad(
        291.34 + 1.844379 * k
    )

    A12 = deg_to_rad(
        161.72 + 24.198154 * k
    )

    A13 = deg_to_rad(
        239.56 + 25.513099 * k
    )

    A14 = deg_to_rad(
        331.55 + 3.592518 * k
    )

    A15 = deg_to_rad(
        275.45 + 2.309908 * k
    )

    planetary = (
        0.000325 * math.sin(A1)
        + 0.000165 * math.sin(A2)
        + 0.000164 * math.sin(A3)
        + 0.000126 * math.sin(A4)
        + 0.000110 * math.sin(A5)
        + 0.000062 * math.sin(A6)
        + 0.000060 * math.sin(A7)
        + 0.000056 * math.sin(A8)
        + 0.000047 * math.sin(A9)
        + 0.000042 * math.sin(A10)
        + 0.000040 * math.sin(A11)
        + 0.000037 * math.sin(A12)
        + 0.000035 * math.sin(A13)
        + 0.000023 * math.sin(A14)
        + 0.000023 * math.sin(A15)
    )

    return jde + corr + planetary


# =========================================================
# MOMENT GŁÓWNEJ FAZY
# =========================================================

def phase_event(
    year,
    month,
    day,
    phase_number
):

    jd = julian_day(
        year,
        month,
        day,
        12,
        0
    )

    k = (
        jd - 2451550.09766
    ) / 29.530588861

    k = math.floor(k) + phase_number

    return phase_jd(k)


# =========================================================
# NAZWA FAZY DLA KONKRETNEGO DNIA
# =========================================================

def get_day_phase_name(
    year,
    month,
    day,
    utc_offset=UTC_OFFSET
):

    jd_start = (
        julian_day(
            year,
            month,
            day,
            0,
            0
        )
        - utc_offset / 24.0
    )

    jd_end = jd_start + 1.0

    # -----------------------------------------------------
    # Sprawdzamy, czy jedna z głównych faz przypada
    # dokładnie na ten dzień.
    # -----------------------------------------------------

    phases = (
        (0.0, "NÓW"),
        (0.25, "PIERWSZA KWADRA"),
        (0.5, "PEŁNIA"),
        (0.75, "OSTATNIA KWADRA")
    )

    for phase_value, name in phases:

        # Sprawdzamy kilka sąsiednich lunacji.
        base_k = (
            (
                jd_start
                - 2451550.09766
            )
            / 29.530588861
        )

        base_k = math.floor(base_k)

        for shift in (-1, 0, 1):

            k = (
                base_k
                + shift
                + phase_value
            )

            event = phase_jd(k)

            if (
                jd_start
                <= event
                < jd_end
            ):
                return name


    # -----------------------------------------------------
    # Nie ma głównej fazy tego dnia.
    #
    # Bierzemy południe lokalne i określamy fazę
    # pośrednią.
    # -----------------------------------------------------

    jd_noon = (
        julian_day(
            year,
            month,
            day,
            12,
            0
        )
        - utc_offset / 24.0
    )

    # Przybliżona faza na podstawie najbliższych
    # głównych wydarzeń.
    k = (
        (
            jd_noon
            - 2451550.09766
        )
        / 29.530588861
    )

    cycle = k % 1.0

    if cycle < 0.25:
        return "ROSNĄCY SIERP"

    if cycle < 0.50:
        return "ROSNĄCY GARB"

    if cycle < 0.75:
        return "MALEJĄCY GARB"

    return "MALEJĄCY SIERP"


# =========================================================
# DOKŁADNA FAZA DLA DATY + GODZINY
# =========================================================

def moon_phase(
    year,
    month,
    day,
    hour=12,
    minute=0,
    utc_offset=UTC_OFFSET
):

    # Lokalny czas -> UTC
    jd = (
        julian_day(
            year,
            month,
            day,
            hour,
            minute
        )
        - utc_offset / 24.0
    )

    # -----------------------------------------------------
    # Znajdź poprzednią główną fazę.
    # -----------------------------------------------------

    k_float = (
        jd - 2451550.09766
    ) / 29.530588861

    k_base = math.floor(
        k_float * 4.0
    ) / 4.0

    previous_jd = None
    previous_phase = None

    next_jd = None
    next_phase = None

    # Kilka punktów wokół aktualnej daty.
    for i in range(-2, 8):

        k = k_base + i * 0.25

        event_jd = phase_jd(k)

        phase_value = k % 1.0

        if event_jd <= jd:

            if (
                previous_jd is None
                or event_jd > previous_jd
            ):

                previous_jd = event_jd
                previous_phase = phase_value

        else:

            if (
                next_jd is None
                or event_jd < next_jd
            ):

                next_jd = event_jd
                next_phase = phase_value


    # -----------------------------------------------------
    # Interpolacja pomiędzy głównymi fazami.
    # -----------------------------------------------------

    fraction = (
        jd - previous_jd
    ) / (
        next_jd - previous_jd
    )

    phase = (
        previous_phase
        + 0.25 * fraction
    ) % 1.0


    # -----------------------------------------------------
    # OŚWIETLENIE
    # -----------------------------------------------------

    illumination = (
        0.5
        * (
            1.0
            - math.cos(
                2.0 * PI * phase
            )
        )
    )

    illumination_percent = (
        illumination * 100.0
    )


    # -----------------------------------------------------
    # NAZWA DLA DNIA
    # -----------------------------------------------------

    phase_name = get_day_phase_name(
        year,
        month,
        day,
        utc_offset
    )


    return (
        phase,
        illumination_percent,
        phase_name
    )