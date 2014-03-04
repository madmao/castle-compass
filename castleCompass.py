import math

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

gps_lat = 38.854068
gps_long = -104.806474
nearest_castle = None
nearest_distance = None

for castle in castles:
    distance = distance_on_unit_sphere(gps_lat, gps_long, castle[0], castle[1]) * 3963.1676  # earth radius in miles
    if nearest_distance is None or distance < nearest_distance:
        nearest_castle = castle
        nearest_distance = distance


print("Nearest White Castle : " + str(nearest_castle) + ", " + str(int(nearest_distance)) + " miles")