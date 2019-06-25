# RPi_modular
Open source project around Raspberry Pi and eurorack Modular systems 

# installation
flasher raspbian stretch lite sur une carte micro Sd d'au moins 8Gb.
https://www.raspberrypi.org/downloads/raspbian/

les nom d'utilisateur et mots de passe par défauts sont respectivement : <b>pi</b> et <b>raspberry</b>.<br/>
Par defaut, le clavier est parametré en mode qwerty, pour modifier ça et parametrer la connexion wifi, utiliser la commande <code>sudo raspi-config</code><br/>

toujours dans l'utilitaire raspi-config, selectionner <b>interfacing options</b> --> <b>serial</b> --> <b>no</b> --> <b>yes</b><br/>
puis <b>spi</b> --> <b>yes</b><br/>
ainsi que <b>boot</b> --> <b>autologin</b><br/>
connectez vous à internet depuis <b>networking options</b>.

<br/><i>installation du driver audio :</i>

lancer la commande
<code>sudo rpi-update</code><br/>
dans <b>/boot/config.txt</b>
commenter <code>dtparam=audio=on</code><br/> et ajouter <code>dtoverlay=audioinjector-wm8731-audio</code><br/>
utiliser l'utilitaire alsamixer pour ouvrir les entrées et sorties (hifi output et capture)


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
