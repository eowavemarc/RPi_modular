import time
import OSC
import threading
import cfg
import sys
import os
import psutil
import subprocess


#______________________________ DISPLAY FONCTIONS ______________________________#
	
def display_inputs1():
	"""displays the names and values of the encoders on the page on screen 1"""
	
	cfg.disp.clear()
	cfg.draw.rectangle((0,0,cfg.width,cfg.height), outline=0, fill=0)
	for j in range(4):	
		try:
			cfg.draw.text((0+64*(j%2),cfg.fontOffset+32*int(j/2)), cfg.encoder[j+4*cfg.activePage].name, font=cfg.font, fill=255)
			cfg.draw.rectangle((0+65*(j%2),18+32*int(j/2),63+64*(j%2),31+32*int(j/2)),outline=1,fill=0)
			cfg.draw.rectangle((1+65*(j%2),20+32*int(j/2),cfg.encoder[j+4*cfg.activePage].value*63/127+65*(j%2),29+32*int(j/2)),outline=1,fill=1)
		except:
			pass
	
	cfg.disp.image(cfg.image)
	cfg.disp.display()
	
def display_input2():
	""" 
	Displays the active value and send osc messages of encoder on the screen 2
	"""
	try:
		#######
		# display
		#######
		cfg.disp2.clear()
		cfg.draw2.rectangle((0,0,cfg.width,cfg.height), outline=0, fill=0)

		cfg.draw2.line([4,22,124,22], fill=255)
		cfg.draw2.text((3,5+cfg.fontOffset), cfg.encoder[cfg.last_pot+(cfg.activePage)*4].name, font=cfg.font, fill=255)
		adaptedValue = (cfg.encoder[cfg.last_pot+(cfg.activePage)*4].value/127.0)*(cfg.encoder[cfg.last_pot+(cfg.activePage)*4].max-cfg.encoder[cfg.last_pot+(cfg.activePage)*4].min)+cfg.encoder[cfg.last_pot+(cfg.activePage)*4].min
		if abs(adaptedValue) < 100:
			cfg.draw2.text((40,33+cfg.fontOffset), str(float(int(adaptedValue*10))/10), font=cfg.number_font, fill=255)
		elif abs(adaptedValue) < 1000:
			cfg.draw2.text((30,33+cfg.fontOffset), str(int(adaptedValue)), font=cfg.number_font, fill=255)
		else:
			cfg.draw2.text((20,33+cfg.fontOffset), str(int(adaptedValue)), font=cfg.number_font, fill=255)
		cfg.draw2.text((104,46+cfg.fontOffset), str(cfg.encoder[cfg.last_pot+(cfg.activePage)*4].unit), font=cfg.font, fill=255)
		cfg.disp2.image(cfg.image2)
		cfg.disp2.display()

		#######
		# send osc
		#######
		client.sendto(OSC.OSCMessage("/"+cfg.encoder[cfg.last_pot+(cfg.activePage)*4].name, adaptedValue), app)
		
	except:
		pass

	
def display_page():
	"""displays on the screen 1 the page you're switching to"""
	
	cfg.disp.clear()
	cfg.draw.rectangle((0,0,cfg.width,cfg.height),outline=0,fill=0)
	cfg.draw.line([4,22,124,22], fill=255)
	cfg.draw.text((3,2+cfg.fontOffset),'page',font=cfg.font,fill=1)
	cfg.draw.text((30,35+cfg.fontOffset),str(cfg.activePage+1)+'/'+str(cfg.numberOfPages),font=cfg.number_font,fill=1)
	cfg.disp.image(cfg.image)
	cfg.disp.display()

	
def display_fft():
	""" 
	displays the fft visualization on screen 2
	"""
	cfg.disp2.clear()
	cfg.draw2.rectangle((0,0,cfg.width,cfg.height), outline=0, fill=0)
	for i in range(128):
		try:
			cfg.draw2.line((i, (cfg.fft[i]-1)*-64,i,64), fill=1)
		except:
			pass
	cfg.disp2.image(cfg.image2)
	cfg.disp2.display()

def display_waveform():
	""" 
	display the waveform on screen 2
	"""
	cfg.disp2.clear()
	cfg.draw2.rectangle((0,0,cfg.width,cfg.height), outline=0, fill=0)
	for i in range(128):
		try:
			cfg.draw2.line((i, cfg.waveform[i]*32+32,i+1,cfg.waveform[i+1]*32+32), fill=1)
		except:
			pass
	cfg.disp2.image(cfg.image2)
	cfg.disp2.display()
	
def display_cpu():
	"""display cpu on screen 2"""
	
	cpu = psutil.cpu_percent()
	cfg.draw2.rectangle((0,0,cfg.width,cfg.height), outline=0, fill=0)
	cfg.draw2.text((10,21+cfg.fontOffset), "CPU : "+str(int(cpu)), font=cfg.font, fill=255)
	cfg.draw2.rectangle((100,0,112,63),outline=1,fill=0)
	cfg.draw2.rectangle((102,63-cpu*0.63,110,63),outline=1,fill=1)
	cfg.disp2.image(cfg.image2)
	cfg.disp2.display()
	cfg.disp2.clear()


def display_cv_in():
	""" 
	visualization of incoming CV on screen 2
	"""
	cfg.draw2.rectangle((0,0,cfg.width,cfg.height), outline=0, fill=0)

	cfg.draw2.rectangle((0,0,23,52), outline=255, fill=0)
	cfg.draw2.rectangle((2,52-cfg.cv[0]*0.52,21,52), outline=255, fill=255)

	cfg.draw2.rectangle((26,0,49,52), outline=255, fill=0)
	cfg.draw2.rectangle((28,52-cfg.cv[1]*0.52,47,52), outline=255, fill=255)

	cfg.draw2.rectangle((52,0,75,52), outline=255, fill=0)
	cfg.draw2.rectangle((54,52-cfg.cv[2]*0.52,73,52), outline=255, fill=255)

	cfg.draw2.rectangle((78,0,101,52), outline=255, fill=0)
	cfg.draw2.rectangle((80,52-cfg.cv[3]*0.52,99,52), outline=255, fill=255)

	cfg.draw2.rectangle((104,0,127,52), outline=255, fill=0)
	cfg.draw2.rectangle((106,52-cfg.cv[4]*0.52,125,52), outline=255, fill=255)

	cfg.draw2.rectangle((0,56,61,63), outline=255, fill=0)
	cfg.draw2.rectangle((2,58,59,61), outline=cfg.gate_1, fill=cfg.gate_1)

	cfg.draw2.rectangle((66,56,127,63), outline=255, fill=0)
	cfg.draw2.rectangle((68,58,125,61), outline=cfg.gate_2, fill=cfg.gate_2)

	cfg.disp2.image(cfg.image2)
	cfg.disp2.display()
	cfg.disp2.clear()
	
	
def display_activeSwitch(switch):
	"""display the value and name of a switch when it is pressed (screen 2)"""
	
	cfg.draw2.rectangle((0,0,cfg.width,cfg.height),outline=0, fill=0)
	cfg.draw2.line([4,22,124,22], fill=255)
	cfg.draw2.text((3,4+cfg.fontOffset),cfg.switch[switch+cfg.activePage].name,font=cfg.font,fill=1)
	cfg.draw2.text((10,34+cfg.fontOffset),cfg.switch[switch+cfg.activePage].stateNames[cfg.switch[switch.cfg.activePage].state],font=cfg.number_font,fill=1)
	cfg.disp2.image(cfg.image2)
	cfg.disp2.display()
	cfg.disp2.clear()

def display_allSwitchs():
	"""display the values of the 4 switch on the page (screen 2)"""
	
	cfg.draw2.rectangle((0,0,cfg.width,cfg.height), outline=0, fill=0)
	cfg.draw2.text((0,13+cfg.fontOffset), str(cfg.switch[0+4*cfg.activePage].stateNames[cfg.switch[0+4*cfg.activePage].state]), font=cfg.font, fill=255)
	cfg.draw2.text((64,13+cfg.fontOffset), str(cfg.switch[1+4*cfg.activePage].stateNames[cfg.switch[1+4*cfg.activePage].state]), font=cfg.font, fill=255)
	cfg.draw2.text((0,43+cfg.fontOffset), str(cfg.switch[2+4*cfg.activePage].stateNames[cfg.switch[2+4*cfg.activePage].state]), font=cfg.font, fill=255)
	cfg.draw2.text((64,43+cfg.fontOffset), str(cfg.switch[3+4*cfg.activePage].stateNames[cfg.switch[3+4*cfg.activePage].state]), font=cfg.font, fill=255)
	cfg.disp2.image(cfg.image2)
	cfg.disp2.display()
	cfg.disp2.clear()
	
	
def display_patchList1():
	"""displays the patchs list on screen 1"""
	
	cfg.draw.rectangle((0,0,cfg.width,cfg.height), outline=0, fill=0)
	cfg.draw.rectangle((0,7+int(cfg.menu_line)*16,6,10+int(cfg.menu_line)*16), outline=0, fill=255)
	cfg.draw.rectangle((121,7+int(cfg.menu_line)*16,127,10+int(cfg.menu_line)*16), outline=0, fill=1)
	for j in range(4):
		try:
			if cfg.device == 0:
				cfg.draw.text((12, cfg.fontOffset-2+16*j), cfg.patch_list_sd[j+int(cfg.menu_line_offset)], font=cfg.font, fill=255)
			else:
				cfg.draw.text((12, cfg.fontOffset-2+16*j), cfg.patch_list_usb[j+int(cfg.menu_line_offset)], font=cfg.font, fill=255)
		except:
			pass
	cfg.disp.image(cfg.image)
	cfg.disp.display()
	cfg.disp.clear
	

def display_patchList2():
	"""displays what's left of the patchs list on screen 2"""
	
	cfg.draw2.rectangle((0,0,cfg.width,cfg.height), outline=0, fill=0)
	cfg.draw2.rectangle((0,7+(int(cfg.menu_line)*16)-64,6,10+(int(cfg.menu_line)*16)-64), outline=0, fill=255)
	cfg.draw2.rectangle((121,7+(int(cfg.menu_line)*16)-64,127,10+(int(cfg.menu_line)*16)-64), outline=0, fill=1)
	for j in range(4):
		try:
			if cfg.device == 0:
				cfg.draw2.text((12, cfg.fontOffset-2+16*j), cfg.patch_list_sd[j+4+int(cfg.menu_line_offset)], font=cfg.font, fill=255)
			else:
				cfg.draw2.text((12, cfg.fontOffset-2+16*j), cfg.patch_list_usb[j+4+int(cfg.menu_line_offset)], font=cfg.font, fill=255)
		except:
			pass
	cfg.disp2.image(cfg.image2)
	cfg.disp2.display()
	cfg.disp2.clear()

		
#______________________________ OSC FONCTIONS ______________________________#

app = (cfg.send_address)
client = OSC.OSCClient()
client.connect(cfg.send_address)
client.sendto(OSC.OSCMessage("/echo", 1), app)

def change_waveform(addr, tags, stuff, source):
	""" 
	changes the values of the list containing the array/waveform 
	"""
	cfg.waveform = stuff


def change_fft(addr, tags, stuff, source):
	""" 
	changes the values of the list containing the array/waveform 
	"""
	cfg.fft = stuff
	
def change_encoder_value(addr, tags, stuff, source):
	for i in range(len(cfg.encoder)):
		if '/'+cfg.encoder[i].name == addr :
			cfg.encoder[i].value = (stuff[0]-cfg.encoder[i].min)/(cfg.encoder[i].max-cfg.encoder[i].min)*127
			client.sendto(OSC.OSCMessage("/"+cfg.encoder[i].name, stuff[0]), app)
def handlingOsc():
	for i in range(len(cfg.encoder)):
		server.addMsgHandler("/"+cfg.encoder[i].name, change_encoder_value)

def oscSendSwitch(switch,state):
	try:
		client.sendto(OSC.OSCMessage("/"+cfg.switch[switch+cfg.activePage*4].name,cfg.switch[switch+cfg.activePage*4].stateNames[state]), app)
		cfg.switch[switch+cfg.activePage*4].state = state
	except:
		pass


#______________________________ OTHER FONCTIONS ______________________________#

def moveCursor(val):
	if cfg.menu_line == 0 and val < 0:
		cfg.menu_line_offset = max((cfg.menu_line_offset + val),0)
	elif cfg.menu_line == 7 and val > 0:
		if cfg.device == 0:
			cfg.menu_line_offset = max(min((cfg.menu_line_offset + val),len(cfg.patch_list_sd)-8),0)
		else:
			cfg.menu_line_offset = max(min((cfg.menu_line_offset + val),len(cfg.patch_list_usb)-8),0)
	else:
		cfg.menu_line = min(max((cfg.menu_line + val),0),7)
		
	
def display_patchScreen1():
	if cfg.actPage == 1:
		display_page()
	else:
		display_inputs1()

def display_patchScreen2():
	if cfg.act == 1:
		display_input2()
		cfg.act = 0
	elif cfg.actSwitch != -1:
		try:
			display_activeSwitch(cfg.actSwitch)
		except:
			pass
	elif cfg.timedAct==0:
		try:
			if cfg.display_mode[cfg.activePage]=='cv_in':
				display_cv_in()
		except:
			pass
		try:
			if cfg.display_mode[cfg.activePage]=='cpu':
				display_cpu()
		except:
			pass
		try:
			if cfg.display_mode[cfg.activePage]=='waveform':
				display_waveform()
		except:
			pass
		try:
			if cfg.display_mode[cfg.activePage]=='fft':
				display_fft()
		except:
			pass
		try:
			if cfg.display_mode[cfg.activePage]=='switchStates':
				display_allSwitchs()
		except:
			pass


##################
#                #
#     serial     #
#                #
##################

def serial():
	while True:
		serialMsg = cfg.serialLoop()
		if serialMsg[0] == 191:
			if serialMsg[1] < 9:		#switchs
				if serialMsg[2]==1:

					if serialMsg[1]>4:	#switchs des encodeurs
						try:
							cfg.actSwitch = serialMsg[1]-5
							cfg.switch[serialMsg[1]-5+cfg.activePage*4].state = (cfg.switch[serialMsg[1]-5+cfg.activePage*4].state + 1)%cfg.switch[serialMsg[1]-5+cfg.activePage*4].numStates
							oscSendSwitch(serialMsg[1]-5+cfg.activePage*4,cfg.switch[serialMsg[1]-5+cfg.activePage*4].state)
						except:
							pass

					elif serialMsg[1]==1: #bouton 'down'
						if cfg.changingPatch == 0:
							cfg.activePage = (cfg.activePage - 1)%cfg.numberOfPages
							cfg.actPage = 1
						else:
							moveCursor(1)

					elif serialMsg[1]==2:	#bouton 'sortie'
						if cfg.changingPatch == 0:
							cfg.ledOn()
							os.system("pkill pd &")
							cfg.activePage = 0
							"""fermer le serveur osc ?"""

							cfg.readPatchList()
							cfg.changingPatch = 1
							cfg.ledOff()
							
					elif serialMsg[1]==3:	#bouton 'selection'
						if cfg.changingPatch == 1:
							try:
								cfg.ledOn()
								if cfg.device==1:
									cfg.read_config_file(cfg.usbPath+cfg.patch_list_usb[int(cfg.menu_line)+int(cfg.menu_line_offset)]+"/conf.txt")
									handlingOsc()
									os.system('pd -path /usr/lib/pd/extra/osc -path '+cfg.usbPath+'../ -nogui -alsamidi -mididev 1 '+cfg.usbPath+cfg.patch_list_usb[int(cfg.menu_line)+int(cfg.menu_line_offset)]+'/main.pd &')
								else:
									cfg.read_config_file(cfg.sdPath+cfg.patch_list_sd[int(cfg.menu_line)+int(cfg.menu_line_offset)]+"/conf.txt")
									handlingOsc()
									os.system('pd -path /usr/lib/pd/extra/osc -path '+cfg.sdPath+'../ -nogui -alsamidi -mididev 1 '+cfg.sdPath+cfg.patch_list_sd[int(cfg.menu_line)+int(cfg.menu_line_offset)]+'/main.pd &')
								time.sleep(2)
								os.system("aconnect 20:0 128:0")
								cfg.changingPatch = 0
								cfg.ledOff()
							except:
								cfg.readPatchList()
								cfg.ledOff()

					elif serialMsg[1]==4: #bouton 'up'
						if cfg.changingPatch == 0:
							cfg.activePage = (cfg.activePage + 1)%cfg.numberOfPages
							cfg.actPage = 1
						else:
							moveCursor(-1)
				else:
					cfg.actPage=0
					cfg.actSwitch=-1

			elif serialMsg[1] < 24:		#Encoders going up
				if cfg.changingPatch == 1:
					moveCursor(serialMsg[2]*0.1)
				elif cfg.changingPatch == 0:
					cfg.last_pot=serialMsg[1]-20
					try:
						cfg.encoder[serialMsg[1]-20+cfg.activePage*4].value = max(min(cfg.encoder[serialMsg[1]-20+cfg.activePage*4].value - serialMsg[2]*0.5,127),0)
					except:
						pass
					cfg.act = 1
					cfg.timedAct = 1

			elif serialMsg[1] < 28:		#Encoders going down
				if cfg.changingPatch == 1:
					moveCursor(-serialMsg[2]*0.1)
				elif cfg.changingPatch == 0:
					cfg.last_pot=serialMsg[1]-24
					try:
						cfg.encoder[serialMsg[1]-24+cfg.activePage*4].value = max(min(cfg.encoder[serialMsg[1]-24+cfg.activePage*4].value + serialMsg[2]*0.5,127),0)
					except:
						pass
					cfg.act = 1
					cfg.timedAct = 1

			elif serialMsg[1] < 50:		#Gates
				if serialMsg[1] == 30:
					cfg.gate_1 = serialMsg[2]
					try:
						client.sendto(OSC.OSCMessage("/gate"+str(1), serialMsg[2]), app)
					except:
						pass
				else:
					cfg.gate_2 = serialMsg[2]
					try:
						client.sendto(OSC.OSCMessage("/gate"+str(2), serialMsg[2]), app)
					except:
						pass

			else:		#CVs
				cfg.cv[serialMsg[1]-50] = serialMsg[2]
				try:
					client.sendto(OSC.OSCMessage("/cv"+str(serialMsg[1]-49), serialMsg[2]), app)
				except:
					pass

		else:	#midi-jack
			try:
				client.sendto(OSC.OSCMessage("/midi", serialMsg), app)
			except:
				pass

serialThread = threading.Thread(target=serial)
serialThread.start()

##################
#                #
#  timer thread  #
#                #
##################

def timer():
	while  True:
		if cfg.act==0:
			time.sleep(1)
			cfg.timedAct = 0

timerThread = threading.Thread(target=timer)
timerThread.start()


##################
#                #
#      OSC       #
#                #
##################

server = OSC.OSCServer(cfg.receive_address)
server.addDefaultHandlers

server.addMsgHandler("/fft",  change_fft)
server.addMsgHandler("/waveform",  change_waveform)

oscServer = threading.Thread(target=server.serve_forever)
oscServer.start()


####################
#                  #
# starting display #
#                  #
####################

cfg.readPatchList()

cfg.ledOff()

while True:
	while(cfg.changingPatch==1): #affichage de la liste des patchs
		 display_patchList1() 
		 display_patchList2()
		 time.sleep(0.03)

	while(cfg.changingPatch==0): #affichage des infos du patch actif
		 display_patchScreen2()
		 display_patchScreen1() 
		 time.sleep(0.03)
