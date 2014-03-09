import os
import math



class CastleDirectory:

    CSV_DIR = '/home/pi/castlecompass/csv/'

    def __init__(self):

        self.csv_list = None
        self.castle_array = None
        self.current_csv = None

        self.get_csv_list()
        if len(self.csv_list) == 0:
            raise Exception("No CSV files found.")

        self.choose_castle(self.csv_list[0])

    def current_csv_friendly_name(self):
        return self.current_csv.replace(".csv", '')

    def get_csv_list(self):
        print("CSVs Found:")
        self.csv_list = []
        for file_name in os.listdir(self.CSV_DIR):
            if file_name.endswith(".csv"):
                self.csv_list.append(file_name)
                print file_name

    def select_next(self):
        current_index = self.csv_list.index(self.current_csv)
        next_index = current_index+1
        if next_index >= len(self.csv_list):
            next_index = 0

        next_csv = self.csv_list[next_index]
        self.choose_castle(next_csv)

    def choose_castle(self, castle_name):
        print("Castle Selected " + castle_name)
        self.current_csv = castle_name
        self.castle_array = []
        with open(self.CSV_DIR + self.current_csv) as f:
            content = f.readlines()
            for line in content:
                split_string = line.split(',')
                lat = float(split_string[0])
                lng = float(str.strip(split_string[1]))
                self.castle_array.append([lat, lng])

    def find_nearest_castle(self, latitude, longitude):

        nearest_castle = None
        nearest_distance = None

        for castle in self.castle_array:
            distance = self.distance_on_unit_sphere(latitude, longitude, castle[0], castle[1]) * 3963.1676  # earth radius in miles
            if nearest_distance is None or distance < nearest_distance:
                nearest_castle = castle
                nearest_distance = distance

        return nearest_castle, nearest_distance

    def distance_on_unit_sphere(self, lat1, long1, lat2, long2):
        # Convert latitude and longitude to
        # spherical coordinates in radians.
        degrees_to_radians = math.pi / 180.0

        # phi = 90 - latitude
        phi1 = (90.0 - lat1) * degrees_to_radians
        phi2 = (90.0 - lat2) * degrees_to_radians

        # theta = longitude
        theta1 = long1 * degrees_to_radians
        theta2 = long2 * degrees_to_radians

        # Compute spherical distance from spherical coordinates.

        # For two locations in spherical coordinates
        # (1, theta, phi) and (1, theta, phi)
        # cosine( arc length ) =
        #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
        # distance = rho * arc length

        cos = (math.sin(phi1) * math.sin(phi2) * math.cos(theta1 - theta2) +
               math.cos(phi1) * math.cos(phi2))
        arc = math.acos(cos)

        # Remember to multiply arc by the radius of the earth
        # in your favorite set of units to get length.
        return arc