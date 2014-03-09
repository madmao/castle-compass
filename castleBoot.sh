cd /home/pi/castlecompass
sudo gpsd /dev/ttyAMA0 -F /var/run/gpsd.sock
sudo python castleCompass.py