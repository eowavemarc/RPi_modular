from PIL import Image, ImageDraw, ImageFont
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306 as adafruit
import os
import serial
import struct

folderPath = "/media/usb/"

#____________________CONFIG____________________#

display_mode = []

class Encoder:
    def __init__(self, name, min, max, unit):
		self.name = name
		self.value = 0
		self.min = float(min)
		self.max = float(max)
		self.unit = unit
encoder = []

class Switch:
    def __init__(self,name, stateNames):
        self.name = name
        self.stateNames = stateNames
        self.numStates = len(self.stateNames)
switch = []

def read_config_file(fichier):
    global display_mode, encoder, switch, display_value, numberOfPages

    for i in range(len(encoder)):
	del encoder[0]

    fichier = open(fichier,"r")
    data = fichier.read()
    fichier.close()
    data = data.split(" ")
    newdata = ''
    for i in range(len(data)):
        newdata = newdata + str(data[i])
    newdata = newdata.split("\t")
    
    data = ''
    for i in range(len(newdata)):
		data = data + str(newdata[i])
    
    data = data.split('\n')
    newdata = ''

    for i in range(len(data)):
        newdata = newdata + data[i]

    data = newdata.split('=')

    for i in range(len(data)):
	if data[i]=="display_mode":
            display_mode = data[i+1].split(';')

        if data[i]=="encoder":
		tempdata = data[i+1].split(';')
		for j in range(len(tempdata)):
			temp = tempdata[j].split(',')
			try:
				encoder.append(Encoder(temp[0],temp[1],temp[2],temp[3]))
			except:
				pass

        if data[i]=="switch":
		try:
			tempdata = data[i+1].split(';')
		except:
			pass
		for i in range(len(tempdata)):
			temp = tempdata[i].split(',')
			switchName = temp[0]
			del temp[0]
			try:
				switch.append(Switch(switchName,temp))
			except:
				pass

	numberOfPages = max(len(display_mode),len(encoder)//4+1,len(switch)//4+1)


#____________________SERIAL____________________#

ser = serial.Serial(port='/dev/ttyS0',baudrate=115200)

def serialLoop():
        seri = [0]*3
	while True:
		line = ser.read()
		line = struct.unpack('B',line)
		if line[0] > 127:
                        seri[0] = line[0]
                        for i in range(2):
                            line = ser.read()
                            line = struct.unpack('B',line)
                            seri[i+1] = line[0]
			return(seri)


#____________________SCREEN____________________#

# Raspberry Pi pin configuration:
DC1 = 23
RST1 = 24
SPI_PORT1 = 0
SPI_DEVICE1 = 0

DC2 = 12
RST2 = 16
SPI_PORT2 = 0
SPI_DEVICE2 = 1

# 128x32 display with hardware SPI:
disp = adafruit.SSD1306_128_64(rst=RST1, dc=DC1, spi=SPI.SpiDev(SPI_PORT1, SPI_DEVICE1, max_speed_hz=8000000))
disp2 = adafruit.SSD1306_128_64(rst=RST2, dc=DC2, spi=SPI.SpiDev(SPI_PORT2, SPI_DEVICE2, max_speed_hz=8000000))

disp.begin()
disp2.begin()

disp.clear()
disp2.clear()

disp.display()
disp2.display()

width = disp.width
height = disp.height

image = Image.new('1', (width, height))
image2 = Image.new('1', (width, height))

draw = ImageDraw.Draw(image)
draw2 = ImageDraw.Draw(image2)

top = 0
bottom = height

#HERE YOU CAN CHANGE THE FONTS
font_folder = "/home/pi/font/"

font = ImageFont.truetype(font_folder+"Laffayette_Comic_Pro.ttf",15)
number_font = ImageFont.truetype(font_folder+"Laffayette_Comic_Pro.ttf", 32)
small_number_font = ImageFont.truetype(font_folder+"Laffayette_Comic_Pro.ttf", 11)
name_font = ImageFont.load_default()



#____________________FLAGS____________________#

display_table_flag = 1

act = 0
timedAct = 0
actPage = 0


#____________________VALUES & CV____________________#

cv = [51]*5

gate_1 = 0

gate_2 = 1

#____________________FORMS AND GRAPHICS____________________#

#Positions for the graphical elements

pot1_pos = [0, 0, 36, 36]
pot2_pos = [29, 27, 65, 63]
pot3_pos = [58, 0, 94, 36]
pot4_pos = [87, 27, 123, 63]

rec1_pos = [15, 38, 21, 43]
rec2_pos = [44, 20, 50, 25]
rec3_pos = [73, 38, 79, 43]
rec4_pos = [102, 20, 108, 25]

rec_fill = [0]*4


#____________________UTILITIES____________________#

changingPatch = 1

menu_line = 1

receive_address = '127.0.0.1', 9998
send_address = '127.0.0.1', 9001

activePage = 0

numberOfPages = 1

table = []

#____________________SYSTEM____________________#

def readPatchList():
	global patch_list
	patch_list = sorted(os.listdir(folderPath)) #list of atmnt folder in the previous folder
	i = 0
	while(i<len(patch_list)):
		if patch_list[i]!=patch_list[i].replace('.',''):
			del patch_list[i]
			i -= 1
		i += 1
