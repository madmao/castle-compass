import math
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate

castles = []

with open('CastleJustLatLongs.csv') as f:
    content = f.readlines()
    for line in content:
        split_string = line.split(',')
        lat = float(split_string[0])
        lng = float(str.strip(split_string[1]))
        castles.append([lat, lng])


def distance_on_unit_sphere(lat1, long1, lat2, long2):

    # Convert latitude and longitude to
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0

    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians

    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians

    # Compute spherical distance from spherical coordinates.

    # For two locations in spherical coordinates
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) =
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length

    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) +
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos(cos)

    # Remember to multiply arc by the radius of the earth
    # in your favorite set of units to get length.
    return arc


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
    percentage_around = input_bearing/360 + 0.03125
    if percentage_around > 1:
        percentage_around -= 1.0
    cardinal_index = int(percentage_around*len(cardinals))
    return cardinals[cardinal_index]


gps_lat = 38.854068
gps_long = -104.806474
nearest_castle = None
nearest_distance = None

for castle in castles:
    distance = distance_on_unit_sphere(gps_lat, gps_long, castle[0], castle[1]) * 3963.1676  # earth radius in miles
    if nearest_distance is None or distance < nearest_distance:
        nearest_castle = castle
        nearest_distance = distance

bearing = angle_from_coordinate(gps_lat, gps_long, nearest_castle[0], nearest_castle[1])
cardinal = bearing_to_cardinal(bearing)

print("Nearest White Castle: " + str(nearest_castle) + ", " + str(int(nearest_distance)) + " miles to the " + cardinal)

lcd = Adafruit_CharLCDPlate()
lcd.clear()
lcd.message("White Castle\n" + str(int(nearest_distance)) + " miles " + cardinal)
