MOON_W = 300
MOON_H = 300

DARK_SIDE_BRIGHTNESS = 0.30


# =========================================================
# DOKŁADNIE TA SAMA KONWERSJA, KTÓRA DZIAŁAŁA
# W test_moon_raw.py
# =========================================================

colors = bytearray(256 * 2)

for g in range(256):

    r = g >> 3
    gr = g >> 2
    b = g >> 3

    c = (
        (r << 11)
        |
        (gr << 5)
        |
        b
    )

    colors[2 * g] = c & 0xff
    colors[2 * g + 1] = c >> 8


# =========================================================
# GENEROWANIE
# =========================================================

print("Przygotowywanie tekstur...")

with open("moon.raw", "rb") as source, \
     open("moon_bright.raw", "wb") as bright, \
     open("moon_dark.raw", "wb") as dark:

    for y in range(MOON_H):

        gray_row = source.read(MOON_W)

        if len(gray_row) != MOON_W:
            raise RuntimeError(
                "moon.raw ma zly rozmiar"
            )

        bright_row = bytearray(MOON_W * 2)
        dark_row = bytearray(MOON_W * 2)

        for x in range(MOON_W):

            gray = gray_row[x]

            # ---------------------------------------------
            # JASNA STRONA
            # ---------------------------------------------

            i = gray << 1

            bright_row[2 * x] = colors[i]
            bright_row[2 * x + 1] = colors[i + 1]


            # ---------------------------------------------
            # CIEMNA STRONA
            # ---------------------------------------------

            dark_gray = int(
                gray * DARK_SIDE_BRIGHTNESS
            )

            i = dark_gray << 1

            dark_row[2 * x] = colors[i]
            dark_row[2 * x + 1] = colors[i + 1]


        bright.write(bright_row)
        dark.write(dark_row)


print("Gotowe.")
print()
print("moon_bright.raw:", 300 * 300 * 2, "bajtow")
print("moon_dark.raw:  ", 300 * 300 * 2, "bajtow")