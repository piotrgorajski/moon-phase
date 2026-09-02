# =========================================================
# GEOMETRIA KSIĘŻYCA
# =========================================================

CX = 160.0
CY = 149.5
RADIUS = 149.5


def touch_to_screen(raw_x, raw_y):
    x = 320-int((raw_x-430)*320/3270)
    y = int((raw_y-430)*480/3270)

    if(x>320):
        x = 320
    elif x<0:
        x = 0
    if(y>480):
        y = 480
    elif y<0:
        y = 0
    y = 480 - y 

    return x, y


def get_touch(LCD):
    touch = LCD.touch_get()

    if touch is None:
        return None

    raw_x = int(touch[0])
    raw_y = int(touch[1])
    
    return touch_to_screen(raw_x, raw_y)


def get_action(LCD):
    touch = get_touch(LCD)

    if touch is None:
        return None

    x, y = touch
    
    # Debug logx
    print("x = " + str(x) + " y = " + str(y))

    # Dolny pasek
    if y >= 310:
        if x < 160:
            return "PREVIOUS_DAY"
        else:
            return "NEXT_DAY"

    # Obszar Księżyca
    dx = x - CX
    dy = y - CY

    # Margines 20 px wewnątrz rzeczywistej tarczy
    touch_radius = RADIUS - 20
    
    # Debug Logs
    # print("DX = " + str(dx) + " SQ = " + str(dx*dx))
    # print("DX = " + str(dy) + " SQ = " + str(dy*dy))
    # print("SQ SUM = " + str(dx*dx+dy*dy))
    # print("RADIUS = " + str(touch_radius) + " SQ = " + str(touch_radius*touch_radius))
    
    if dx * dx + dy * dy <= touch_radius * touch_radius:
        return "TODAY"

    return None
