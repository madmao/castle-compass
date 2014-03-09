import math
from time import sleep

from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
from CastleGPS import CastleGPS
from CastleDirectory import CastleDirectory

def angle_from_coordinate(lat1, long1, lat2, long2):
    longitudinal_distance = (long2 - long1)

    y = math.sin(longitudinal_distance) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(longitudinal_distance)

    bearing_result = math.atan2(y, x)

    bearing_result = math.degrees(bearing_result)
    bearing_result = (bearing_result + 360) % 360
    bearing_result = 360 - bearing_result

    return bearing_result

def bearing_to_cardinal(input_bearing):
    cardinals = ['E', 'ENE', 'NE', 'NNE', 'N', 'NNW', 'NW', 'WNW', 'W', 'WSW', 'SW', 'SSW', 'S', 'SSE', 'SE', 'ESE']
    percentage_around = input_bearing / 360 + 0.03125
    if percentage_around > 1:
        percentage_around -= 1.0
    cardinal_index = int(percentage_around * len(cardinals))
    return cardinals[cardinal_index]

lcd = Adafruit_CharLCDPlate()
lcd.clear()
lcd.message("CastleCompass!")

gps = CastleGPS()
gps.start()

castles = CastleDirectory()

print('ran past gps start')

while True:

    if gps.current_latitude is not None:
        nearest_castle, nearest_distance = castles.find_nearest_castle(gps.current_latitude, gps.current_longitude)
        bearing = angle_from_coordinate(gps.current_latitude, gps.current_longitude, nearest_castle[0], nearest_castle[1])
        cardinal = bearing_to_cardinal(bearing)

        print("Nearest " + castles.current_csv + ": " + str(nearest_castle) + ", " + str(int(nearest_distance)) + " miles to the " + cardinal)
        lcd.clear()
        lcd.message(castles.current_csv + "\n" + str(nearest_distance) + "M " + cardinal)
    else:
        print('No Gps Signal Yet...')

    sleep(1)