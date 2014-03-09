import math
from time import sleep
import sys

from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
from CastleGPS import CastleGPS
from CastleDirectory import CastleDirectory


def calculate_initial_compass_bearing(pointA, pointB):
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = math.radians(pointA[0])
    lat2 = math.radians(pointB[0])

    diffLong = math.radians(pointB[1] - pointA[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing


def bearing_to_cardinal(input_bearing):
    cardinals = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    percentage_around = (float(input_bearing) / 360.0) + 0.03125
    if percentage_around > 1.0:
        percentage_around -= 1.0
    cardinal_index = int(percentage_around * len(cardinals))
    return cardinals[cardinal_index]

def pi_log(msg):
    print(msg)
    lcd.clear()
    lcd.message(msg)
    sleep(0.5)

def test_bearings():
    bears = [0.0, 90, 180, 270, 359]
    for b in bears:
        print(str(b) + ' > ' + bearing_to_cardinal(b))

test_bearings()

try:
    lcd = Adafruit_CharLCDPlate()
    pi_log('   Castle\n     Compass')
    sleep(2)
    pi_log('Starting GPS...')
    gps = CastleGPS()
    gps.start()
    pi_log('Started GPS')

    pi_log('Getting Castles...')
    castles = CastleDirectory()
    pi_log('Got Castles')
    pi_log('Awaiting 3D\nGPS Fix...')

    last_message = ''
    while True:
        if gps.current_latitude is not None:
            nearest_castle, nearest_distance = castles.find_nearest_castle(gps.current_latitude, gps.current_longitude)
            bearing = calculate_initial_compass_bearing((gps.current_latitude, gps.current_longitude,), (nearest_castle[0], nearest_castle[1],))
            cardinal = bearing_to_cardinal(bearing)

            new_message = castles.current_csv_friendly_name() + "\n" + str(round(nearest_distance, 4)) + " Mi " + cardinal
            if new_message != last_message:

                print("Nearest " + castles.current_csv + ": " + str(nearest_castle) + ", " + str(int(nearest_distance)) + " miles to the " + cardinal)
                last_message = new_message
                lcd.clear()
                lcd.message(new_message)

            if lcd.buttonPressed(lcd.SELECT):
                castles.select_next()
                sleep(0.1)

        else:
            print('Acquiring 3D GPS Lock...')

        sleep(0.2)
except IOError:
    sleep(1)
    pi_log("IOError Exception!")
except KeyboardInterrupt:
    pi_log("  Cheeseburger\n    Shutdown!")
except Exception:
    sleep(1)
    pi_log("Exception!")
    type, value, traceback = sys.exc_info()
    pi_log(str(type))
    pi_log(str(value.strerror))
    print('Error opening %s: %s' % (value.filename, value.strerror))