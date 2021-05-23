# main.py -- put your code here!
from pyb import SPI, Pin
import pyb
import vt100

##########################################################################

# UART STM32F4 Discovery Shield
uart = pyb.UART(2)
uart.init(115200, bits=8, parity=None, stop=1)

# INITIALISATION SPI 1
CS = Pin("PE3", Pin.OUT_PP)
SPI_1 = SPI( 1, SPI.MASTER, baudrate=50000, polarity=0, phase=0)

##########################################################################

def MoveWrite(uart,x,y,caracteres):
        vt100.move(uart,x,y)
        uart.write(caracteres)

def convert_value(high,low):
    value = (high << 8) | low
    if value & (1 << 15):
        value = value - (1 << 16)
    # value = value * 0.06
    return value

def get_axis(uart, address):
	result = 0

	value = [0, 0]

	CS.low()
	SPI_1.send(0x80 | address+1)
	value[0] = SPI_1.recv(1)[0]
	CS.high()

	CS.low()
	SPI_1.send(0x80 | address)
	value[1] = SPI_1.recv(1)[0]
	CS.high()

	result = convert_value(value[0], value[1])

	result /= 16384

	return result

def wait_pin_change(pin, etat_souhaite):
    # wait for pin to change value
    # it needs to be stable for a continuous 20ms
    active = 0
    while active < 50:
        if pin.value() == etat_souhaite:
            active += 1
        else:
            active = 0
        pyb.delay(1)

##########################################################################

def SetBorders():

    # LEFT and RIGHT
    for i in range (1, MAX_HEIGHT):
        vt100.move(uart, 1, i)
        uart.write("\u2551")
        vt100.move(uart, MAX_WIDTH, i)
        uart.write("\u2551")

    # DOWN
    for i in range (1, MAX_WIDTH):
        vt100.move(uart, i, MAX_HEIGHT)
        uart.write("\u2550")

    # CORNER UP LEFT
    vt100.move(uart, 1, 1)
    uart.write("\u2554")
    # CORNER DOWN LEFT
    vt100.move(uart, 1, MAX_HEIGHT)
    uart.write("\u255A")
    # CORNER UP RIGHT
    vt100.move(uart, MAX_WIDTH, 1)
    uart.write("\u2557")
    # CORNER DOWN LEFT
    vt100.move(uart, MAX_WIDTH, MAX_HEIGHT)
    uart.write("\u255D")


def Spaceship(posX,y):
    MoveWrite(uart, posX , y, " ==U== ")


class Ennemies():
    def __init__(self, x, y, dir):
        self.x = x
        self.y = y
        self.dir = dir 
        MoveWrite(uart, self.x, self.y," |++X++| ")
    def Moving(self):
        if (self.x >= 80):
            self.dir = -1
            self.x = self.x + self.dir
            MoveWrite(uart, self.x, self.y, "         ")
            self.y = self.y +2 
            MoveWrite(uart, self.x, self.y, " |++X++| ")
        elif (self.x <= 5):
            self.dir = +1
            self.x = self.x + self.dir
            MoveWrite(uart, self.x, self.y, "         ")
            self.y = self.y + 2 
            MoveWrite(uart, self.x, self.y, " |++X++| ")
        else:
            self.x = self.x + self.dir
            MoveWrite(uart, self.x, self.y, " |++X++| ")
        
        # DEBUG
        print(self.x, self.y)

        
def initFleet(Fleet):
    for i in range(5):    
        Fleet[i] = Ennemies(i*9 + 7*(i+1), 4, 1)

##########################################################################

leds = [pyb.LED(1), pyb.LED(2)]
push_button = Pin("PA0", Pin.IN, Pin.PULL_DOWN)

CS.low()
SPI_1.send(0x00 | 0x20)
SPI_1.send(0x77)
CS.high()

##########################################################################

# MAX DIMENSIONS
MAX_WIDTH = 90
MAX_HEIGHT = 40

# Max dimensions /2
posX = 45
posY = 20

# LOSE line limit
lose = 40

##########################################################################

vt100.clear_screen(uart)
SetBorders() 

Fleet = [0,0,0,0,0]
initFleet(Fleet)

while True:

    result = get_axis(uart, 0x28)
    if (result >= 0.25):
        leds[0].on()
        leds[1].off()
        posX += 1
    elif (result <= -0.25):
        leds[0].off()
        leds[1].on()
        posX -= 1
    else:
        leds[0].off()
        leds[1].off()

    if (MAX_WIDTH-7 >= posX >= 2):
        Spaceship(posX, MAX_HEIGHT-1)

    for i in range(5):
        Fleet[i].Moving()

    if  push_button.value():
        for i in range (-MAX_HEIGHT+2, 1):
            MoveWrite(uart, posX+3, -i, "*")
            pyb.delay(20)
            MoveWrite(uart, posX+3, -i, " ")
        wait_pin_change(push_button, 0)

    # IF LOSE
    if (Fleet[0].y >= lose):
        vt100.clear_screen(uart)
        vt100.move(uart, posX, posY)
        uart.write("LOSE - GAME OVER")
        break
    if (Fleet[4].y >= lose):
        vt100.clear_screen(uart)
        vt100.move(uart, posX, posY)
        uart.write("LOSE - GAME OVER")
        break

    pyb.delay(100)
