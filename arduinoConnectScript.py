import serial
import time

# Set up the serial connection to the Arduino
# Ensure the correct port and baud rate are specified
arduino = serial.Serial(port='COM3', baudrate=9600, timeout=1)

# Allow time for the connection to establish
time.sleep(2)

# Function to send a command to the Arduino
def send_command(command):
    arduino.write(command.encode())  # Send the command as a byte string
    time.sleep(1)  # Wait for a second before sending the next command

# Send commands to control the motor
send_command('F')  # Spin motor forward
time.sleep(2)       # Wait for 2 seconds
#send_command('S')   # Stop the motor
#time.sleep(1)       # Wait for 1 second
#send_command('B')   # Spin motor backward
#time.sleep(2)       # Wait for 2 seconds
send_command('S')   # Stop the motor
time.sleep(1)       # Wait for 1 second

# Close the serial connection when done
arduino.close()

# C:\Users\ethan\notebooksmlprojects\.ipynb_checkpoints\arduinoConnectScript.py