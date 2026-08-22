from machine import Pin,SPI,PWM
import framebuf
import time
import os

PICO_RP2040 = True
PICO_RP2350 = not PICO_RP2040

LCD_DC   = 8
LCD_CS   = 9
LCD_SCK  = 10
LCD_MOSI = 11
LCD_MISO = 12
LCD_BL   = 13
LCD_RST  = 15
TP_CS    = 16
TP_IRQ   = 17

class LCD_3inch5(framebuf.FrameBuffer):

    def __init__(self):
        self.RED   =   0x07E0
        self.GREEN =   0x001f
        self.BLUE  =   0xf800
        self.WHITE =   0xffff
        self.BLACK =   0x0000
        
        self.rotate = 0   # Set the rotation Angle to 0°, 90°, 180° and 270°
        
        if self.rotate == 0 or self.rotate == 180:
            self.width = 320
            self.height = 240
        else:
            self.width = 480
            self.height = 160
            
        self.cs = Pin(LCD_CS,Pin.OUT)
        self.rst = Pin(LCD_RST,Pin.OUT)
        self.dc = Pin(LCD_DC,Pin.OUT)
        
        self.tp_cs =Pin(TP_CS,Pin.OUT)
        self.irq = Pin(TP_IRQ,Pin.IN)
        
        self.cs(1)
        self.dc(1)
        self.rst(1)
        self.tp_cs(1)
        self.spi = SPI(1,6_000_000)
        print(self.spi)  
        self.spi = SPI(1,baudrate=40_000_000,sck=Pin(LCD_SCK),mosi=Pin(LCD_MOSI),miso=Pin(LCD_MISO))
        print(self.spi)      
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()

        
    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        #self.spi.write(bytearray([0X00]))
        self.spi.write(bytearray([buf]))
        self.cs(1)


    def init_display(self):
        """Initialize dispaly"""  
        self.rst(1)
        time.sleep_ms(5)
        self.rst(0)
        time.sleep_ms(10)
        self.rst(1)
        time.sleep_ms(5)
        self.write_cmd(0x21)
        
        self.write_cmd(0xC2)
        self.write_data(0x33)
        
        self.write_cmd(0XC5)
        self.write_data(0x00)
        self.write_data(0x1e)
        self.write_data(0x80)
        
        self.write_cmd(0xB1)
        self.write_data(0xB0)
        
        self.write_cmd(0XE0)
        self.write_data(0x00)
        self.write_data(0x13)
        self.write_data(0x18)
        self.write_data(0x04)
        self.write_data(0x0F)
        self.write_data(0x06)
        self.write_data(0x3a)
        self.write_data(0x56)
        self.write_data(0x4d)
        self.write_data(0x03)
        self.write_data(0x0a)
        self.write_data(0x06)
        self.write_data(0x30)
        self.write_data(0x3e)
        self.write_data(0x0f)
        
        self.write_cmd(0XE1)
        self.write_data(0x00)
        self.write_data(0x13)
        self.write_data(0x18)
        self.write_data(0x01)
        self.write_data(0x11)
        self.write_data(0x06)
        self.write_data(0x38)
        self.write_data(0x34)
        self.write_data(0x4d)
        self.write_data(0x06)
        self.write_data(0x0d)
        self.write_data(0x0b)
        self.write_data(0x31)
        self.write_data(0x37)
        self.write_data(0x0f)
        
        self.write_cmd(0X3A)
        self.write_data(0x55)
        
        self.write_cmd(0x11)
        time.sleep_ms(120)
        self.write_cmd(0x29)
        
        self.write_cmd(0xB6)
        self.write_data(0x00)
        self.write_data(0x62)
        
        self.write_cmd(0x36) # Sets the memory access mode for rotation
        if self.rotate == 0:
            self.write_data(0x88)
        elif self.rotate == 180:
            self.write_data(0x48)
        elif self.rotate == 90:
            self.write_data(0xe8)
        else:
            self.write_data(0x28)
    def show_up(self):
        if self.rotate == 0 or self.rotate == 180:
            self.write_cmd(0x2A)
            self.write_data(0x00)
            self.write_data(0x00)
            self.write_data(0x01)
            self.write_data(0x3f)
             
            self.write_cmd(0x2B)
            self.write_data(0x00)
            self.write_data(0x00)
            self.write_data(0x00)
            self.write_data(0xef)
        else:
            self.write_cmd(0x2A)
            self.write_data(0x00)
            self.write_data(0x00)
            self.write_data(0x01)
            self.write_data(0xdf)
            
            self.write_cmd(0x2B)
            self.write_data(0x00)
            self.write_data(0x00)
            self.write_data(0x00)
            self.write_data(0x9f)
            
            
        self.write_cmd(0x2C)
        
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)
    def show_down(self):
        if self.rotate == 0 or self.rotate == 180:
            self.write_cmd(0x2A)
            self.write_data(0x00)
            self.write_data(0x00)
            self.write_data(0x01)
            self.write_data(0x3f)
             
            self.write_cmd(0x2B)
            self.write_data(0x00)
            self.write_data(0xf0)
            self.write_data(0x01)
            self.write_data(0xdf)
        else:
            self.write_cmd(0x2A)
            self.write_data(0x00)
            self.write_data(0x00)
            self.write_data(0x01)
            self.write_data(0xdf)
            
            self.write_cmd(0x2B)
            self.write_data(0x00)
            self.write_data(0xA0)
            self.write_data(0x01)
            self.write_data(0x3f)
            
        
        self.write_cmd(0x2C)
        
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)
    def bl_ctrl(self,duty):
        pwm = PWM(Pin(LCD_BL))
        pwm.freq(1000)
        if(duty>=100):
            pwm.duty_u16(65535)
        else:
            pwm.duty_u16(655*duty)

    def touch_get(self): 
        if self.irq() == 0:
            self.spi = SPI(1,4_000_000,sck=Pin(LCD_SCK),mosi=Pin(LCD_MOSI),miso=Pin(LCD_MISO))
            self.tp_cs(0)
            X_Point = 0
            Y_Point = 0
            for i in range(0,3):
                self.spi.write(bytearray([0XD0]))
                Read_date = self.spi.read(2)
                time.sleep_us(10)
                X_Point=X_Point+(((Read_date[0]<<8)+Read_date[1])>>3)
                
                self.spi.write(bytearray([0X90]))
                Read_date = self.spi.read(2)
                Y_Point=Y_Point+(((Read_date[0]<<8)+Read_date[1])>>3)

            X_Point=X_Point/3
            Y_Point=Y_Point/3
            
            self.tp_cs(1) 
            self.spi = SPI(1,40_000_000,sck=Pin(LCD_SCK),mosi=Pin(LCD_MOSI),miso=Pin(LCD_MISO))
            Result_list = [X_Point,Y_Point]
            #print(Result_list)
            return(Result_list)

def draw_moon_horizontal(phase):

    cx = 240
    cy = 100
    r = 50

    import math

    # Kąt fazy
    angle = 2 * math.pi * phase

    # Określa położenie terminatora.
    # -1 = pełnia
    #  0 = kwadra
    # +1 = cienki sierp
    terminator = math.cos(angle)

    for y in range(cy - r, cy + r + 1):

        dy = y - cy

        # Szerokość tarczy w tym wierszu
        half_width = math.sqrt(r * r - dy * dy)

        # Położenie terminatora dla tego wiersza
        boundary = terminator * half_width

        for x in range(cx - r, cx + r + 1):

            dx = x - cx

            # Czy jesteśmy wewnątrz okrągłej tarczy?
            if dx * dx + dy * dy <= r * r:

                if phase < 0.5:

                    # Rosnący Księżyc:
                    # światło po prawej stronie
                    if dx >= boundary:
                        LCD.pixel(x, y, LCD.WHITE)

                else:

                    # Malejący Księżyc:
                    # światło po lewej stronie
                    if dx <= -boundary:
                        LCD.pixel(x, y, LCD.WHITE)


def draw_moon_part(phase, global_y_start):

    import math

    # Pozycja Księżyca na fizycznym ekranie 320 x 480
    cx = 160
    cy = 145
    radius = 140

    # Nów
    if phase <= 0.001 or phase >= 0.999:
        return

    # cos:
    # 0.0  ->  1
    # 0.25 ->  0
    # 0.5  -> -1
    # 0.75 ->  0
    # 1.0  ->  1
    k = math.cos(2 * math.pi * phase)

    # Po pełni odwracamy kierunek terminatora
    if phase >= 0.5:
        k = -k

    # Bufor ma 240 pikseli wysokości
    for local_y in range(240):

        # Pozycja Y na fizycznym ekranie
        global_y = global_y_start + local_y

        dy = global_y - cy

        if abs(dy) > radius:
            continue

        # Szerokość Księżyca w tym wierszu
        half_width = math.sqrt(
            radius * radius - dy * dy
        )

        left = int(cx - half_width)
        right = int(cx + half_width)

        # Zakrzywiony terminator
        terminator_x = cx + k * half_width

        if phase < 0.5:

            # NÓW -> PEŁNIA
            # światło przybywa z prawej

            start_x = int(terminator_x)

            if start_x < left:
                start_x = left

            if start_x > right:
                start_x = right

            for x in range(start_x, right + 1):
                LCD.pixel(x, local_y, LCD.WHITE)

        else:

            # PEŁNIA -> NÓW
            # światło znika z prawej

            end_x = int(terminator_x)

            if end_x < left:
                end_x = left

            if end_x > right:
                end_x = right

            for x in range(left, end_x + 1):
                LCD.pixel(x, local_y, LCD.WHITE)


def draw_moon(phase):

    # =========================
    # GÓRNE 240 px EKRANU
    # =========================

    LCD.fill(LCD.BLACK)

    draw_moon_part(phase, 0)

    LCD.show_up()


    # =========================
    # DOLNE 240 px EKRANU
    # =========================

    LCD.fill(LCD.BLACK)

    draw_moon_part(phase, 240)

    LCD.show_down()

# ============================================
# MAIN
# ============================================

if __name__ == '__main__':

    LCD = LCD_3inch5()
    LCD.bl_ctrl(100)

    # TESTUJ TĘ WARTOŚĆ
    phase = 0.0

    draw_moon(phase)

    while True:
        time.sleep(1)

#     phases = [
#         0.0,
#         0.1,
#         0.2,
#         0.25,
#         0.3,
#         0.4,
#         0.5,
#         0.6,
#         0.7,
#         0.75,
#         0.8,
#         0.9,
#         1.0
#     ]
# 
#     while True:
# 
#         for phase in phases:
# 
#             print("phase =", phase)
# 
#             draw_moon(phase)
# 
#             time.sleep(1)
