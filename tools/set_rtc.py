from machine import Pin, I2C
import binascii


I2C_PORT = 0
I2C_SDA = 20
I2C_SCL = 21

RTC_ADDR = 0x68


i2c = I2C(
    I2C_PORT,
    scl=Pin(I2C_SCL),
    sda=Pin(I2C_SDA)
)


def dec_to_bcd(value):
    return ((value // 10) << 4) | (value % 10)


# =========================================================
# USTAWIENIA CZASU
# =========================================================

YEAR = 2026
MONTH = 9
DAY = 7

HOUR = 13
MINUTE = 45
SECOND = 0


# Dzień tygodnia:
# 1 = niedziela
# 2 = poniedziałek
# ...
# 7 = sobota

WEEKDAY = 1


data = bytes([
    dec_to_bcd(SECOND),
    dec_to_bcd(MINUTE),
    dec_to_bcd(HOUR),
    WEEKDAY,
    dec_to_bcd(DAY),
    dec_to_bcd(MONTH),
    dec_to_bcd(YEAR - 2000)
])


i2c.writeto_mem(
    RTC_ADDR,
    0x00,
    data
)


print("RTC ustawiony.")