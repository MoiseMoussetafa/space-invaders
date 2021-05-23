VT100_ESC = '\x1B'

def move(uart, x, y):
	x = str(x)
	y = str(y)
	uart.write(VT100_ESC + '[' + y + ';' + x + 'H')

def clear_screen(uart):
	uart.write(VT100_ESC+'[2J')