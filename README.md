
# Modbus Server with Sensors

This Python script is designed to create a Modbus TCP server that communicates with temperature and water level sensors. It reads data from a DS18B20 temperature sensor and an ADS1115 analog-to-digital converter (ADC) which is connected to an analog water level sensor and makes this data available through Modbus registers.


## Prerequisites

Before running this code, you should ensure you have the following hardware components and Python libraries installed:

### Hardware Requirements

- **DS18B20 Temperature Sensor:** Make sure you have a DS18B20 temperature sensor connected to your Raspberry Pi. The sensor's unique ID should start with '28-'.

- **ADS1115 ADC:** Ensure that you have an ADS1115 analog-to-digital converter connected to your Raspberry Pi for water level measurement. The SCL and SDA pins should be specified correctly in the code.

- **Water Level Sensor:** Make sure that you have a water level sensor connected in line on the Breadboard to the ADC.

- **Breadboard:** The breadboard is required for ensuring connection between the ADC and the Water Level Sensor.

### Python Libraries
Make sure you have the required Python libraries installed:

- **Adafruit_ADS1x15:** This library is used to interface with the ADS1115 ADC.

   ```bash
   pip install Adafruit-ADS1x15
   ```

- **pyModbusTCP:** This library is used to create the Modbus TCP server.

   ```bash
   pip install pyModbusTCP
   ```

## Configuration

1. **Sensor Setup:**
- Ensure that both sensors are attached to the correct ports, ensure that the DS18B20 is recognized by the Raspberry Pi and that the ADS1115 ADC is connected to the correct ports.
2. **Modbus Server Configuration:**
- Specify the desired IP address and port for the Modbus TCP server by replacing the first field in the ModbusServer initialization with your values.





## Usage

Once you have configured the script and ensured that the required hardware is set up, you can run the code. Use the following command:

```bash
sudo python3 sensorToModbus.py
```

The script will start the Modbus TCP server and continuously read temperature and water level sensor data, updating the Modbus input registers with this information.

## Output

The script will output the current temperature in both Celsius and Fahrenheit, as well as the water level sensor value, to the console. It will also update Modbus registers IR1 (for temperature in Celsius), IR2 (for temperature in Fahrenheit), and IR3 (for water level value) with the respective sensor readings. 

## Stopping the Script

You can stop the script by pressing Ctrl+C. This will gracefully shut down the Modbus server and stop the script execution.

Please note that this README provides an overview of the code and its usage. Detailed hardware connections and configurations may vary depending on your specific setup.
