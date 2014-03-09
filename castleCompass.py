import math
from time import sleep

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


def castle_picker_ui(ada_lcd, castle_directory):
    ada_lcd.clear()
    ada_lcd.message("Pick castle:\n" + castle_directory.current_csv_friendly_name())
    sleep(0.5)
    while ada_lcd.buttonPressed(ada_lcd.SELECT) == 0:
        if ada_lcd.buttonPressed(ada_lcd.UP) or ada_lcd.buttonPressed(ada_lcd.DOWN) or ada_lcd.buttonPressed(ada_lcd.LEFT) or ada_lcd.buttonPressed(ada_lcd.RIGHT):
            castle_directory.select_next()
            ada_lcd.clear()
            ada_lcd.message("Pick castle:\n" + castle_directory.current_csv_friendly_name())
            sleep(0.5)

    print("Picked: " + castle_directory.current_csv)


def test_bearings():
    bears = [0.0, 90, 180, 270, 359]
    for b in bears:
        print(str(b) + ' > ' + bearing_to_cardinal(b))

test_bearings()

# exit()

lcd = Adafruit_CharLCDPlate()
lcd.clear()
lcd.message("CastleCompass!\nAcquiring GPS...")

gps = CastleGPS()
gps.start()

castles = CastleDirectory()

last_message = ''
while True:
    if gps.current_latitude is not None:
        nearest_castle, nearest_distance = castles.find_nearest_castle(gps.current_latitude, gps.current_longitude)
        bearing = calculate_initial_compass_bearing((gps.current_latitude, gps.current_longitude,), (nearest_castle[0], nearest_castle[1],))
        cardinal = bearing_to_cardinal(bearing)

        new_message = castles.current_csv_friendly_name() + "\n" + str(round(nearest_distance, 3)) + " Mi " + cardinal
        if new_message != last_message:

            print("Nearest " + castles.current_csv + ": " + str(nearest_castle) + ", " + str(int(nearest_distance)) + " miles to the " + cardinal)
            last_message = new_message
            lcd.clear()
            lcd.message(new_message)

        if lcd.buttonPressed(lcd.SELECT):
            castle_picker_ui(lcd, castles)

    else:
        print('Acquiring 3D GPS Lock...')

    sleep(0.2)