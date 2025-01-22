import serial
import time

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

# Give some time for the connection to establish
time.sleep(2)

def switch_channel(channel):
    # Switch command channel
    command = f'SW {channel}\r\n'
    ser.write(command.encode())
    
    # Wait for the response
    response = ser.read(8)  # Adjust byte size as needed
    print(f"Switched to Channel {channel}: {response.decode()}")

# Switch between the first three channels
while(1):
    for channel in range(1):
        switch_channel(channel + 1)
        time.sleep(1) 

# Close the serial connection
ser.close()
