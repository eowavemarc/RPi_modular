import time
import OSC
import threading
import cfg
import sys
import os
import psutil
import subprocess


#______________________________ DISPLAY FONCTIONS ______________________________#

def display_loading_screen():
	""" 
	displays the classic loading screen and the name of the patch you're opening.
	this fonction is called by open_patch() and change_patch().
	"""
	cfg.draw.rectangle((0,0,cfg.width,cfg.height), outline=0, fill=0)
	cfg.draw.text((5, 10), "LOADING", font=cfg.font, fill=255)
	cfg.draw.text((10, 20), ".", font=cfg.font, fill=255)
	cfg.disp.image(cfg.image)
	cfg.disp.display()
	cfg.disp.clear()
	cfg.draw2.rectangle((0,0,cfg.width,cfg.height), outline=0, fill=0)
	cfg.draw2.text((5, 10), "LOADING", font=cfg.font, fill=255)
	cfg.draw2.text((10, 20), ".", font=cfg.font, fill=255)
	cfg.disp2.image(cfg.image2)
	cfg.disp2.display()
	cfg.disp2.clear()
	time.sleep(0.5)
	cfg.draw.text((5, 10), "LOADING", font=cfg.font, fill=255)
	cfg.draw.text((10, 20), ". .", font=cfg.font, fill=255)
	cfg.disp.image(cfg.image)
	cfg.disp.display()
	cfg.disp.clear()
	cfg.draw2.text((5, 10), "LOADING", font=cfg.font, fill=255)
	cfg.draw2.text((10, 20), ". .", font=cfg.font, fill=255)
	cfg.disp2.image(cfg.image2)
	cfg.disp2.display()
	cfg.disp2.clear()
	time.sleep(0.5)
	cfg.draw.text((5, 10), "LOADING", font=cfg.font, fill=255)
	cfg.draw.text((10, 20), ". . .", font=cfg.font, fill=255)
	cfg.disp.image(cfg.image)
	cfg.disp.display()
	cfg.disp.clear()
	cfg.draw2.text((5, 10), "LOADING", font=cfg.font, fill=255)
	cfg.draw2.text((10, 20), ". . .", font=cfg.font, fill=255)
	cfg.disp2.image(cfg.image2)
	cfg.disp2.display()
	cfg.disp2.clear()
	time.sleep(0.5)
	cfg.draw.rectangle((0,0,cfg.width,cfg.height), outline=0, fill=0)
	cfg.disp.image(cfg.image)
	cfg.disp.display()
	cfg.disp.clear()
	cfg.draw2.rectangle((0,0,cfg.width,cfg.height), outline=0, fill=0)
	cfg.disp2.image(cfg.image2)
	cfg.disp2.display()
	cfg.disp2.clear()

	
def display_inputs1():
	""" 
	Displays a set of four values on one page.
	"""

	pot_angle = [135]*4

	for i in range(4):
		try:
			pot_angle[i] = min(max(135+int(cfg.encoder[i+(cfg.activePage)*4].value)*2.12,135),410)
		except:
			pass

	#_______________________________________________________________

	cfg.disp.clear()
	cfg.draw.rectangle((0,0,cfg.width,cfg.height), outline=0, fill=0)

	cfg.draw.chord(cfg.pot1_pos, 0, 405, outline=255, fill=0)
	cfg.draw.pieslice(cfg.pot1_pos, pot_angle[0], pot_angle[0], outline=1,fill=1)
	cfg.draw.chord(cfg.pot2_pos, 0, 405, outline=255, fill=0)
	cfg.draw.pieslice(cfg.pot2_pos, pot_angle[1], pot_angle[1], outline=255,fill=255)
	cfg.draw.chord(cfg.pot3_pos, 0, 405, outline=255, fill=0)
	cfg.draw.pieslice(cfg.pot3_pos, pot_angle[2], pot_angle[2], outline=255,fill=255)
	cfg.draw.chord(cfg.pot4_pos, 0, 405, outline=255, fill=0)
	cfg.draw.pieslice(cfg.pot4_pos, pot_angle[3], pot_angle[3], outline=255,fill=255)

	cfg.draw.rectangle(cfg.rec1_pos, outline=255, fill=cfg.rec1_fill)
	cfg.draw.rectangle(cfg.rec2_pos, outline=255, fill=cfg.rec2_fill)
	cfg.draw.rectangle(cfg.rec3_pos, outline=255, fill=cfg.rec3_fill)
	cfg.draw.rectangle(cfg.rec4_pos, outline=255, fill=cfg.rec4_fill)

	cfg.draw.text((100,4),str(cfg.activePage+1)+'/'+str(cfg.numberOfPages), font=cfg.small_number_font, fill=1)
	cfg.disp.image(cfg.image)
	cfg.disp.display()

	
def display_input2():
	""" 
	Displays the active value and send osc messages of encoder
	"""
	try:
		#######
		# display
		#######
		cfg.disp2.clear()
		cfg.draw2.rectangle((0,0,cfg.width,cfg.height), outline=0, fill=0)

		cfg.draw2.line([4,22,124,22], fill=255)
		cfg.draw2.text((3,6), cfg.encoder[cfg.last_pot+(cfg.activePage)*4].name, font=cfg.font, fill=255)
		adaptedValue = (cfg.encoder[cfg.last_pot+(cfg.activePage)*4].value/127.0)*(cfg.encoder[cfg.last_pot+(cfg.activePage)*4].max-cfg.encoder[cfg.last_pot+(cfg.activePage)*4].min)+cfg.encoder[cfg.last_pot+(cfg.activePage)*4].min
		if abs(adaptedValue) < 100:
			cfg.draw2.text((40,35), str(int(adaptedValue)), font=cfg.number_font, fill=255)
		elif abs(adaptedValue) < 1000:
			cfg.draw2.text((30,35), str(int(adaptedValue)), font=cfg.number_font, fill=255)
		else:
			cfg.draw2.text((20,35), str(int(adaptedValue)), font=cfg.number_font, fill=255)
		cfg.draw2.text((104,50), str(cfg.encoder[cfg.last_pot+(cfg.activePage)*4].unit), font=cfg.font, fill=255)
		cfg.disp2.image(cfg.image2)
		cfg.disp2.display()

		#######
		# send osc
		#######
		client.sendto(OSC.OSCMessage("/"+cfg.encoder[cfg.last_pot+(cfg.activePage)*4].name, adaptedValue), app)
		
	except:
		pass

	
def display_table():
	""" 
	display the table on the screen
	"""
	cfg.disp2.clear()
	cfg.draw2.rectangle((0,0,cfg.width,cfg.height), outline=0, fill=0)
	for i in range(128):
		try:
			cfg.draw2.point((i, cfg.table[i]*32+32), fill=1)
		except:
			pass
	cfg.disp2.image(cfg.image2)
	cfg.disp2.display()


	
def display_cpu():
	cpu = psutil.cpu_percent()
	cfg.draw2.rectangle((0,0,cfg.width,cfg.height), outline=0, fill=0)
	cfg.draw2.text((10,23), "CPU : "+str(int(cpu)), font=cfg.font, fill=255)
	cfg.draw2.rectangle((100,0,112,63),outline=1,fill=0)
	cfg.draw2.rectangle((102,63-cpu*0.63,110,63),outline=1,fill=1)
	cfg.disp2.image(cfg.image2)
	cfg.disp2.display()
	cfg.disp2.clear()


def display_cv_in():
	""" 
	visualization of incoming CV. 
	"""
	cfg.draw2.rectangle((0,0,cfg.width,cfg.height), outline=0, fill=0)

	cfg.draw2.rectangle((0,0,23,52), outline=255, fill=0)
	cfg.draw2.rectangle((2,cfg.cv[0],21,52), outline=255, fill=255)

	cfg.draw2.rectangle((26,0,49,52), outline=255, fill=0)
	cfg.draw2.rectangle((28,cfg.cv[1],47,52), outline=255, fill=255)

	cfg.draw2.rectangle((52,0,75,52), outline=255, fill=0)
	cfg.draw2.rectangle((54,cfg.cv[2],73,52), outline=255, fill=255)

	cfg.draw2.rectangle((78,0,101,52), outline=255, fill=0)
	cfg.draw2.rectangle((80,cfg.cv[3],99,52), outline=255, fill=255)

	cfg.draw2.rectangle((104,0,127,52), outline=255, fill=0)
	cfg.draw2.rectangle((106,cfg.cv[4],125,52), outline=255, fill=255)

	cfg.draw2.rectangle((0,56,61,63), outline=255, fill=0)
	cfg.draw2.rectangle((2,58,59,61), outline=cfg.gate_1, fill=cfg.gate_1)

	cfg.draw2.rectangle((66,56,127,63), outline=255, fill=0)
	cfg.draw2.rectangle((68,58,125,61), outline=cfg.gate_2, fill=cfg.gate_2)


	cfg.disp2.image(cfg.image2)
	cfg.disp2.display()
	cfg.disp2.clear()


def cursor_move(direction):
	""" 
	moves the cursor up, down or to initialisation
	"""
	if direction == "up":
		cfg.menu_line = (cfg.menu_line - 1)%8

	if direction == "down":
		cfg.menu_line = (cfg.menu_line + 1)%8


#______________________________ OSC FONCTIONS ______________________________#

def change_table(addr, tags, stuff, source):
	""" 
	changes the values of the list containing the array/waveform 
	"""
	cfg.table = stuff

app = ("localhost", 9001)
client = OSC.OSCClient()
client.connect(cfg.send_address)
client.sendto(OSC.OSCMessage("/echo", 1), app)

def oscSendSwitch(switch,state):
	try:
		client.sendto(OSC.OSCMessage("/"+cfg.switch[switch+cfg.activePage*4].name,cfg.switch[switch+cfg.activePage*4].stateNames[state]), app)
	except:
		pass

################
#
def display_patchScreen1():
	display_inputs1()

def display_patchScreen2():
	if cfg.potAct == 1:
		display_input2()
		cfg.potAct = 0
	elif cfg.timedPotAct==0:
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
			if cfg.display_mode[cfg.activePage]=='table':
				display_table()
		except:
			pass


###############
#
def display_patchList1():
	cfg.draw.rectangle((0,0,cfg.width,cfg.height), outline=0, fill=0)
	cfg.draw.rectangle((0,4+cfg.menu_line*16,6,8+cfg.menu_line*16), outline=0, fill=255)
	cfg.draw.rectangle((121,4+cfg.menu_line*16,127,8+cfg.menu_line*16), outline=0, fill=1)
	for j in range(4):
		try:
			cfg.draw.text((12, 2+16*j), cfg.patch_list[j], font=cfg.font, fill=255)
		except:
			pass
	cfg.disp.image(cfg.image)
	cfg.disp.display()
	cfg.disp.clear()

def display_patchList2():
	cfg.draw2.rectangle((0,0,cfg.width,cfg.height), outline=0, fill=0)
	cfg.draw2.rectangle((0,4+(cfg.menu_line*16)-64,6,8+(cfg.menu_line*16)-64), outline=0, fill=255)
	cfg.draw2.rectangle((121,4+(cfg.menu_line*16)-64,127,8+(cfg.menu_line*16)-64), outline=0, fill=1)
	for j in range(4):
		try:
			cfg.draw2.text((12, 2+16*j), cfg.patch_list[j+4], font=cfg.font, fill=255)
		except:
			pass
	cfg.disp2.image(cfg.image2)
	cfg.disp2.display()
	cfg.disp2.clear()


##################
#
# initialisation du seriel
#
##################

def serial():
	while True:
		serialMsg = cfg.serialLoop()
		if serialMsg[0] == 176:
			if serialMsg[2] == 1:
				if serialMsg[1] == 2:
					try:
						cfg.activePage = (cfg.activePage + 1)%cfg.numberOfPages
					except:
						print 'implementer le changement de page'

				if serialMsg[1] == 1:
					if cfg.changingPatch == 0:
						os.system("pkill pd &")
						cfg.activePage = 0
						"""fermer le serveur osc ?"""
						cfg.readPatchList()
						cfg.changingPatch = 1
					elif cfg.changingPatch == 1:
						try:
							os.system('pd -path /usr/lib/pd/extra/osc -nogui '+cfg.folderPath+cfg.patch_list[cfg.menu_line]+'/main.pd &')
							cfg.read_config_file(cfg.folderPath+cfg.patch_list[cfg.menu_line]+"/conf.txt")
							cfg.changingPatch = -1
							display_loading_screen()
							cfg.changingPatch = 0
						except:
							cfg.readPatchList()
				if serialMsg[1] == 5:
					cfg.rec1_fill = (cfg.rec1_fill+1)%2
					oscSendSwitch(0,cfg.rec1_fill)
				if serialMsg[1] == 6:
					cfg.rec2_fill = (cfg.rec2_fill+1)%2
					oscSendSwitch(1,cfg.rec2_fill)
				if serialMsg[1] == 7:
					cfg.rec3_fill = (cfg.rec3_fill+1)%2
					oscSendSwitch(2,cfg.rec3_fill)
				if serialMsg[1] == 8:
					cfg.rec4_fill = (cfg.rec4_fill+1)%2
					oscSendSwitch(3,cfg.rec4_fill)
	
		if serialMsg[0] > 127 and serialMsg[0] < 132:
			if cfg.changingPatch == 1:
				if serialMsg[1] == 1:
					cursor_move('down')
				if serialMsg[1] == 0:
					cursor_move('up')
			elif cfg.changingPatch == 0:
				cfg.last_pot=serialMsg[0]-128
				try:
					cfg.encoder[serialMsg[0]-128+cfg.activePage*4].value = max(min(int(cfg.encoder[serialMsg[0]-128+cfg.activePage*4].value) - (serialMsg[1]*2-1),127),0)
				except:
					pass
				cfg.potAct = 1
				cfg.timedPotAct = 1

serialThread = threading.Thread(target=serial)
serialThread.start()

###################
#
# timer thread
#
###################

def timer():
	while  True:
		if cfg.potAct==0:
			time.sleep(1)
			cfg.timedPotAct = 0

timerThread = threading.Thread(target=timer)
timerThread.start()


###################
#
# initialisation de l'OSC
#
###################

server = OSC.OSCServer(cfg.receive_address)
server.addDefaultHandlers

server.addMsgHandler("/table",  change_table)

oscServer = threading.Thread(target=server.serve_forever)
oscServer.start()


###################
#
# lancement de l'affichage
#
###################

cfg.readPatchList()

while True:
	while(cfg.changingPatch==1): #affichage de la liste des patchs
		 display_patchList1() 
		 display_patchList2()
		 time.sleep(0.03)

	while(cfg.changingPatch==0): #affichage des infos du patch actif
		 display_patchScreen2()
		 display_patchScreen1() 
		 time.sleep(0.03)
