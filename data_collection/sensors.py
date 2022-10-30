'''
ACCESS Lab, hereby disclaims all copyright interest in the program “ACCESS IOT 
Stations” (which collects air and climate data) written by Francesco Paparella, 
Pedro Velasquez.

Copyright (C) 2022 Francesco Paparella, Pedro Velasquez

This file is part of "ACCESS IOT Stations".

"ACCESS IOT Stations" is free software: you can redistribute it and/or modify it under the 
terms of the GNU General Public License as published by the Free Software 
Foundation, either version 3 of the License, or (at your option) any later 
version.

"ACCESS IOT Stations" is distributed in the hope that it will be useful, but WITHOUT ANY 
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR 
A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with 
"ACCESS IOT Stations". If not, see <https://www.gnu.org/licenses/>.

'''

import ACCESS_station_lib as access
import board

# ---------- #
# this file should define 2 things
# sensors: list with ALL the sensors of all types
#           Any beseecher sensor connected to the station must be appended to
#           this list
# gps: unlike the sensors, the gps will be a unique variable with the gps beseecher.
#
# When initializing sensors, ALWAYS use a try-except block in case the RPi 
# fails to start the sensors at boot. The error beseecher class will store any
# error information that comes up and will allow data-collection to report on 
# the error.


try:
    gps = access.GPSbeseecherGPIO() # only 1 GPS
except:
    gps = access.ErrorBeseecher('gps', 'gps', 'Error initializing GPS at boot')

sensors = []

# initialize pm sensors
ports = ['/dev/ttyAMA0', '/dev/ttyAMA1']

for i in range(2):
    try:
        sensors.append(access.NEXTPMbeseecher(port=ports[i], index=i))
    except Exception as e:
        sensors.append(access.ErrorBeseecher('particulate_matter', 'nextpm', str(e), index=i))

i2c = board.I2C()

# initialize air sensors
# bme
try:
    sensors.append(access.BME280beseecher(i2c=i2c, index=0))
except Exception as e:
    error_msg = str(e)
    sensors.append(access.ErrorBeseecher('air_sensor', 'bme280', error_msg, index=0))
# ms8607
try:
    sensors.append(access.MS8607beseecher(i2c=i2c, index=1))
except Exception as e:
    error_msg = str(e)
    sensors.append(access.ErrorBeseecher('air_sensor', 'ms8607', error_msg, index=1))


