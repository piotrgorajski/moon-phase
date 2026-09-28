import framebuf
import math
from lcd_3inch5 import LCD_3inch5

BRIGHT_FILE = "moon_bright565.raw"
DARK_FILE = "moon_dark565.raw"
MOON_W = 300
MOON_H = 300
MOON_X = 10
CHUNK_ROWS = 10
ROW_BYTES = MOON_W * 2
CHUNK_BYTES = ROW_BYTES * CHUNK_ROWS

CX = 160.0
CY = 149.5
RADIUS = 149.5

LCD = LCD_3inch5()
LCD.bl_ctrl(100)

chunk_buffer = bytearray(CHUNK_BYTES)
bright_buffer = bytearray(CHUNK_BYTES)
chunk_view = memoryview(chunk_buffer)
bright_view = memoryview(bright_buffer)

chunk_fb = framebuf.FrameBuffer(
    chunk_buffer,
    MOON_W,
    CHUNK_ROWS,
    framebuf.RGB565
)

row_left = [0] * MOON_H
row_right = [0] * MOON_H
row_half_width = [0.0] * MOON_H

for y in range(MOON_H):
    dy = y - CY
    if abs(dy) > RADIUS:
        continue

    half_width = math.sqrt(
        RADIUS * RADIUS - dy * dy
    )

    row_left[y] = int(
        CX - half_width
    )
    row_right[y] = int(
        CX + half_width
    )
    row_half_width[y] = half_width


def draw_moon_part(
    global_y_start,
    rows,
    bright_file,
    dark_file,
    k,
    phase
):
    phase_is_waxing = phase < 0.5

    for local_y_start in range(0, rows, CHUNK_ROWS):
        chunk_rows = CHUNK_ROWS
        chunk_bytes = chunk_rows * ROW_BYTES

        dark_chunk = chunk_view[:chunk_bytes]
        bright_chunk = bright_view[:chunk_bytes]

        read_dark = dark_file.readinto(dark_chunk)
        if read_dark != chunk_bytes:
            raise RuntimeError(
                "moon_dark565.raw ma zly rozmiar"
            )

        read_bright = bright_file.readinto(bright_chunk)
        if read_bright != chunk_bytes:
            raise RuntimeError(
                "moon_bright565.raw ma zly rozmiar"
            )

        for chunk_y in range(chunk_rows):
            local_y = local_y_start + chunk_y
            global_y = global_y_start + local_y

            left = row_left[global_y]
            right = row_right[global_y]

            if right <= left:
                continue

            half_width = row_half_width[global_y]
            row_start = chunk_y * ROW_BYTES
            terminator_x = CX + k * half_width

            if phase_is_waxing:
                start_x = int(terminator_x)

                if start_x < left:
                    start_x = left
                if start_x > right:
                    start_x = right

                src_start = 2 * (start_x - MOON_X)
                src_end = 2 * (right - MOON_X + 1)
            else:
                end_x = int(terminator_x)

                if end_x < left:
                    end_x = left
                if end_x > right:
                    end_x = right

                src_start = 2 * (left - MOON_X)
                src_end = 2 * (end_x - MOON_X + 1)

            if src_start < 0:
                src_start = 0
            if src_end > ROW_BYTES:
                src_end = ROW_BYTES

            if src_start < src_end:
                start = row_start + src_start
                end = row_start + src_end
                chunk_view[start:end] = bright_chunk[start:end]

        LCD.blit(
            chunk_fb,
            MOON_X,
            local_y_start
        )


def draw_moon(phase):
    if phase < 0.0:
        phase = 0.0
    if phase > 1.0:
        phase = 1.0

    k = math.cos(
        2 * math.pi * phase
    )

    if phase >= 0.5:
        k = -k

    with open(BRIGHT_FILE, "rb") as bright_file, open(DARK_FILE, "rb") as dark_file:
        LCD.fill(LCD.BLACK)

        draw_moon_part(
            0,
            240,
            bright_file,
            dark_file,
            k,
            phase
        )

        LCD.show_up()

        offset = 240 * ROW_BYTES
        bright_file.seek(offset)
        dark_file.seek(offset)

        LCD.fill(LCD.BLACK)

        draw_moon_part(
            240,
            60,
            bright_file,
            dark_file,
            k,
            phase
        )

        LCD.show_down()
