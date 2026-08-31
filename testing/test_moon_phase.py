from moon_phase import moon_phase


tests = [
    (2026, 8, 27, 0, 0),
    (2026, 8, 28, 0, 0),
    (2026, 8, 28, 6, 0),
    (2026, 8, 28, 12, 0),
    (2026, 8, 28, 18, 0),
    (2026, 8, 29, 0, 0),
    (2026, 8, 29, 12, 0),
    (2026, 9, 3, 12, 0),
    (2026, 9, 4, 12, 0),
]


print("MEEUS MOON PHASE TEST")
print()


for (
    year,
    month,
    day,
    hour,
    minute
) in tests:

    phase, illumination, name = moon_phase(
        year,
        month,
        day,
        hour,
        minute,
        2
    )

    print(
        "%04d-%02d-%02d %02d:%02d"
        % (
            year,
            month,
            day,
            hour,
            minute
        )
    )

    print(
        "phase = %.5f"
        % phase
    )

    print(
        "illumination = %.2f%%"
        % illumination
    )

    print(
        "phase name = %s"
        % name
    )

    print()