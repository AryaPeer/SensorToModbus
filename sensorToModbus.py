#!/usr/bin/env python3
import time
import os
import Adafruit_ADS1x15
import struct
from pyModbusTCP.server import ModbusServer, DataBank

# Initialize ADS1115 ADC
adc = Adafruit_ADS1x15.ADS1115()

# Set up GPIO pins
TEMP_SENSOR_PIN = 4

# ADS1115 pins
ADS_SCL_PIN = 3  # SCL pin on ADS1115
ADS_SDA_PIN = 2  # SDA pin on ADS1115

# Modbus TCP server details
server = ModbusServer("", 502, no_block=True)  # Replace first field with your desired IP address and port

def sensor():
    for i in os.listdir('/sys/bus/w1/devices'):
        if i.startswith('28-'):
            ds18b20 = i
            return ds18b20

def read_temp_raw(sensor_id):
    sensor_path = '/sys/bus/w1/devices/{}/w1_slave'.format(sensor_id)
    f = open(sensor_path, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp(sensor_id):
    lines = read_temp_raw(sensor_id)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw(sensor_id)
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

try:
    sensor_id = sensor()
    server.start()
    time.sleep(1)
    print("server start")

    while True:
        # Read temperature
        temp_c, temp_f = read_temp(sensor_id)

        # Convert temperature values to 16-bit signed integers

        # Read water level from ADS1115
        adc.start_adc(0, gain=1)
        time.sleep(0.1)  # Add a small delay for the conversion to complete
        water_level_value = adc.get_last_result()

        # Convert water level value to 16-bit signed integer

        print("Temperature Sensor Value: {:.2f}°C, {:.2f}°F".format(temp_c, temp_f))
        print("Water Level Sensor Value: {}".format(water_level_value))

        # Write temperature and water level values to Modbus input registers
        server.data_bank.set_input_registers(1, [int(temp_c)])  # Input Register 30001 for temperature
        server.data_bank.set_input_registers(2, [int(temp_f)])  # Input Register 30002 for temperature
        server.data_bank.set_input_registers(3, [int(water_level_value)])
        
        time.sleep(0.5)  # Add a delay of 0.5 seconds after setting values

        # Check if all values are set properly
        if (server.data_bank.get_input_registers(1)[0] == int(temp_c) and
            server.data_bank.get_input_registers(2)[0] == int(temp_f) and
            server.data_bank.get_input_registers(3)[0] == int(water_level_value)):
            print("Sent")
        time.sleep(0.5)

except KeyboardInterrupt:
    pass
finally:
    # Stop the Modbus server
    server.stop()
    print("server stop")