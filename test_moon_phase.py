# test_moon_phase.py

from moon_phase import moon_phase


tests = [
    (2026, 8, 28, 0, 0),
    (2026, 8, 28, 12, 0),
    (2026, 8, 28, 18, 0),

    (2026, 8, 29, 0, 0),
    (2026, 8, 29, 12, 0),

    (2026, 9, 3, 12, 0),
]


print("MOON PHASE TEST")
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
        minute
    )


    print(
        "%04d-%02d-%02d %02d:%02d UTC"
        % (
            year,
            month,
            day,
            hour,
            minute
        )
    )

    print(
        "phase = %.4f"
        % phase
    )

    print(
        "illumination = %.1f%%"
        % illumination
    )

    print(
        "phase name = %s"
        % name
    )

    print()