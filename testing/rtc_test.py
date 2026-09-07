from machine import Pin, I2C


I2C_PORT = 0
I2C_SDA = 20
I2C_SCL = 21

RTC_ADDR = 0x68


def bcd_to_dec(value):
    return (value >> 4) * 10 + (value & 0x0F)


i2c = I2C(
    I2C_PORT,
    scl=Pin(I2C_SCL),
    sda=Pin(I2C_SDA)
)


data = i2c.readfrom_mem(
    RTC_ADDR,
    0x00,
    7
)


second = bcd_to_dec(data[0] & 0x7F)
minute = bcd_to_dec(data[1] & 0x7F)
hour   = bcd_to_dec(data[2] & 0x3F)

day   = bcd_to_dec(data[4] & 0x3F)
month = bcd_to_dec(data[5] & 0x1F)
year  = 2000 + bcd_to_dec(data[6])


print(
    "%04d-%02d-%02d %02d:%02d:%02d"
    % (
        year,
        month,
        day,
        hour,
        minute,
        second
    )
)