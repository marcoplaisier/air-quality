import time

from sensirion_i2c_driver import LinuxI2cTransceiver, I2cConnection
from sensirion_i2c_scd import Scd4xI2cDevice


def start_measurements(publish_cb):
    # Connect to the I²C 1 port
    with LinuxI2cTransceiver('/dev/i2c-1') as i2c_transceiver:
        # Create SCD4x device
        scd4x = Scd4xI2cDevice(I2cConnection(i2c_transceiver))

        # Make sure measurement is stopped, else we can't read serial number or
        # start a new measurement
        # scd4x.stop_periodic_measurement()
        #
        # print("scd4x Serial Number: {}".format(scd4x.read_serial_number()))

        scd4x.start_periodic_measurement()

        # Measure every 5 seconds for 5 minute
        while True:
            co2, temperature, humidity = scd4x.read_measurement()
            publish_cb({
                'temperature': temperature,
                'co2': co2,
                'humidity': humidity
            })
            time.sleep(30)
