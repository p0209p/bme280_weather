import time 
import smbus2
import bme280
import psutil
from ISStreamer.Streamer import Streamer
from subprocess import PIPE, Popen

# --------- User Settings ---------
SENSOR_LOCATION_NAME = "ENTER_LOCATION_NAME"
BUCKET_NAME = "ENTER_BUCKET_NAME"
BUCKET_KEY = "KEY"
ACCESS_KEY = "ACCESS_KEY"
# ---------------------------------

# BME280 settings 
port = 1
address = 0x77
bus = smbus2.SMBus(port)
calibration_params = bme280.load_calibration_params(bus, address)

streamer = Streamer(bucket_name=BUCKET_NAME, bucket_key=BUCKET_KEY, access_key=ACCESS_KEY)
while True:
        bme280data = bme280.sample(bus, address, calibration_params)
        humidity = format(bme280data.humidity, ".1f")
        temp_c = bme280data.temperature
        streamer.log(SENSOR_LOCATION_NAME + "Temperature(C)", temp_c)
        streamer.log(SENSOR_LOCATION_NAME + "Humidity(%)", humidity)
        process = Popen(['hostname', '-I'], stdout=PIPE)
        output, _error = process.communicate()
        streamer.log("MechTechLab Temperature Monitor IP Address", output.rstrip().decode())
        streamer.flush()
        time.sleep(1)
