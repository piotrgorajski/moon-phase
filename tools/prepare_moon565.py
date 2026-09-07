MOON_W = 300
MOON_H = 300


def make_rgb565(source_name, output_name):

    # Dokładnie ta sama matematyka RGB565
    # co w działającym rendererze.

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


    with open(source_name, "rb") as src, \
         open(output_name, "wb") as dst:

        while True:

            gray = src.read(MOON_W)

            if not gray:
                break

            if len(gray) != MOON_W:
                raise RuntimeError(
                    source_name + " ma zly rozmiar"
                )


            out = bytearray(
                MOON_W * 2
            )


            for x in range(MOON_W):

                i = gray[x] << 1

                # UWAGA:
                # ODWRACAMY kolejność względem
                # poprzedniej wersji.

                out[2*x] = colors[i + 1]
                out[2*x + 1] = colors[i]


            dst.write(out)


make_rgb565(
    "moon.raw",
    "moon_bright565.raw"
)

make_rgb565(
    "moon_dark.raw",
    "moon_dark565.raw"
)


print("Gotowe.")
print("moon_bright565.raw = 180000 bajtow")
print("moon_dark565.raw   = 180000 bajtow")