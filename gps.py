# gps.py

import serial

def parse_nmea_data(nmea_sentence):
    try:
        parts = nmea_sentence.split(',')
        if parts[0] == "$GPGGA":
            lat = parts[2]; lat_dir = parts[3]
            lon = parts[4]; lon_dir = parts[5]
            return convert_to_decimal(lat, lat_dir), convert_to_decimal(lon, lon_dir)
        return None, None
    except:
        return None, None

def convert_to_decimal(coord, direction):
    if not coord:
        return None
    degrees = float(coord[:2])
    minutes = float(coord[2:]) / 60
    dec = degrees + minutes
    return -dec if direction in ['S', 'W'] else dec

def read_gps_data():
    try:
        with serial.Serial('/dev/ttyTHS1', 57600, timeout=1) as ser:
            while True:
                line = ser.readline().decode('utf-8', errors='replace').strip()
                lat, lon = parse_nmea_data(line)
                if lat and lon:
                    return lat, lon
    except:
        return None, None
