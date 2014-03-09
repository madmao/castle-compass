import threading
import gps
from time import sleep


class CastleGPS(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True

        self.gps = gps.gps("localhost", "2947")
        self.gps.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

        self.current_latitude = None
        self.current_longitude = None
        self.current_speed = None
        self.current_heading = None

    def run(self):
        print("GPS Started")
        while True:
            try:
                report = self.gps.next()
                # print(report)
                if report['class'] == 'TPV':

                    self.current_latitude = report['lat']
                    self.current_longitude = report['lon']
                    self.current_speed = report['speed']
                    self.current_heading = report['track']  # not sure if right attr

                sleep(1)
            except:
                print('GPS exception!')