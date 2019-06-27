# RPi_modular
Open source project around Raspberry Pi and eurorack Modular systems 

# installation
flasher raspbian stretch lite sur une carte micro Sd d'au moins 8Gb.
https://www.raspberrypi.org/downloads/raspbian/

les nom d'utilisateur et mots de passe par défauts sont respectivement : <b>pi</b> et <b>raspberry</b>.<br/>
Par defaut, le clavier est parametré en mode qwerty, pour modifier ça et parametrer la connexion wifi, utiliser la commande <code>sudo raspi-config</code><br/>

wifi : selectinner <b>networking options</b> puis <b> wi-fi</b><br/>
clavier : <b>localisation options</b> puis <b>change keyboard layout</b><br/>
seriel : selectionner <b>interfacing options</b> puis <b>serial</b>, à la question "would you like a login shell to be accessible over serial?", répondre <b>no</b> et à la question "would you like the serial port hardware to be enabled?" répondre <b>yes</b><br/>
spi :  <b>interfacing options</b>, <b>spi</b>, <b>yes</b><br/>
autologin : <b>boot</b>, <b>autologin</b><br/>

<br/><i>installation du driver audio :</i>

lancer la commande
<code>sudo rpi-update</code><br/>
dans <b>/boot/config.txt</b>,
commenter <code>dtparam=audio=on</code> et ajouter <code>dtoverlay=audioinjector-wm8731-audio</code><br/>
Pour ce faire, utiliser la commande <code>sudo nano /boot/config.txt</code> et ajouter un croisillon (#) devant la ligne à commenter.
utiliser l'utilitaire alsamixer pour ouvrir les entrées et sorties :
la touche 'm' permet de muter ou démuter la sortie audio "Output Mixer HiFi" et la touche 'espace' permet d'activer l'entrée audio "Line" qu'on trouve avec la touche f4.

<br/><i>installer les dépendances :</i>

<code>sudo apt-get install --no-install-recommends 
	puredata
	pd-osc
	git
	python-dev
	python-smbus
	python-pil
	python-setuptools
	python-serial
	python-psutil
	usbmount</code><br/>
<code>sudo nano /lib/systemd/system/systemd-udevd.service</code> : remplacer <code>MountFlags=slave</code> par  <code>MountFlags=shared</code>
	
<code>sudo apt-get install --no-install-recommends python-pip</code><br/>
<code>sudo pip install  Adafruit-SSD1306 Adafruit-GPIO</code><br/>
                  
<code>git clone https://github.com/ptone/pyosc.git</code><br/>
<code>cd pyosc</code><br/>
<code>sudo python setup.py install</code><br/>
<code>cd ../</code><br/>

<br/><i>installation du programme principal :</i>

<code>git clone https://github.com/eowavemarc/RPi_modular.git</code><br/>
<code>cd RPi_modular</code><br/>
<code>cp -r * ../</code><br/>
<code>cd ../</code><br/>

<code>sudo rm -r pyosc RPi_modular</code><br/>

<code>sudo nano /etc/rc.local</code> : ajouter <code>python /home/pi/main.py &</code> avant <code>exit 0</code>
