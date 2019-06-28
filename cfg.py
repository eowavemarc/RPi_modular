from PIL import Image, ImageDraw, ImageFont
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306 as adafruit
import os
import serial
import struct


#________________________CONSTANTES______________________________#


device = 1 #0 pour la carte sd et 1 pour la clef usb

usbPath = "/media/usb/"
sdPath = "/home/pi/puredata/exemples/"

font_folder = "/home/pi/font/"

font = ImageFont.truetype(font_folder+"GeosansLight.ttf",18)
number_font = ImageFont.truetype(font_folder+"Laffayette_Comic_Pro.ttf", 32)
name_font = ImageFont.load_default()

fontOffset = -2 #le changement de police necessite parfois un decalage vertical

receive_address = '127.0.0.1', 9998
send_address = '127.0.0.1', 9001



#____________________SYSTEM____________________#

def readPatchList():
	global patch_list_usb, patch_list_sd
	patch_list_usb = sorted(os.listdir(usbPath)) #list of atmnt folder in the previous folder
	patch_list_sd = sorted(os.listdir(sdPath)) #list of atmnt folder in the previous folder
	i = 0
	while(i<len(patch_list_usb)):
		if patch_list_usb[i]!=patch_list_usb[i].replace('.',''):
			del patch_list_usb[i]
			i -= 1
		i += 1
	i = 0
	while(i<len(patch_list_sd)):
		if patch_list_sd[i]!=patch_list_sd[i].replace('.',''):
			del patch_list_sd[i]
			i -= 1
		i += 1

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
        self.state = 0
switch = []

def read_config_file(fichier):
    global display_mode, encoder, switch, display_value, numberOfPages

    display_mode = []
    encoder = []
    switch = []

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

	numberOfPages = max(len(display_mode),(len(encoder)-1)//4+1,(len(switch)-1)//4+1)
	
	
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

def ledOn():
	ser.write(struct.pack('B',191))
	ser.write(struct.pack('B',1))
	ser.write(struct.pack('B',1))

def ledOff():
	ser.write(struct.pack('B',191))
	ser.write(struct.pack('B',1))
	ser.write(struct.pack('B',0))


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

#____________________FLAGS____________________#

display_table_flag = 1

act = 0		#vaut 1 si un encodeur est tourne
timedAct = 0	#idem mais retourne a zero apres un certain temps, pour l'affichage de la valeur de l'encodeur
actPage = 0		#vaut 1 quand le bouton page est enfonce
actSwitch = -1	#vaut la valeur du dernier switch enfonce, retourne a -1 quand un switch est relache

#____________________VALUES & CV____________________#

cv = [51]*5

gate_1 = 0

gate_2 = 0

#____________________UTILITIES____________________#

changingPatch = 1

menu_line = 1
menu_line_offset = 0

activePage = 0

numberOfPages = 1

fft = []
waveform = []
