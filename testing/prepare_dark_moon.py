MOON_W = 300
MOON_H = 300

DARK_SIDE_BRIGHTNESS = 0.30

with open("moon.raw", "rb") as source, \
     open("moon_dark.raw", "wb") as dark:

    data = source.read()

    if len(data) != MOON_W * MOON_H:
        raise RuntimeError(
            "moon.raw ma zly rozmiar"
        )

    for gray in data:

        dark_gray = int(
            gray * DARK_SIDE_BRIGHTNESS
        )

        dark.write(
            bytes((dark_gray,))
        )

print("Gotowe.")
print("moon.raw:", len(data), "bajtow")
print("moon_dark.raw:", MOON_W * MOON_H, "bajtow")