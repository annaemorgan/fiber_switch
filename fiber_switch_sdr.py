import serial
import time
import RPi.GPIO as GPIO

# Set up serial connection
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

# Give some time for the connection to establish
time.sleep(2)

# Configure GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # GPIO 23 as input with pull-up resistor

def switch_channel(channel):
    # Send the switch channel command
    command = f'SW {channel}\r\n'
    ser.write(command.encode())
    
    # Wait for the response
    response = ser.read(8)  # Adjust byte size as needed
    print(f"Switched to Channel {channel}: {response.decode()}")

# Initial states
last_state = GPIO.HIGH  # Last state of GPIO 23
initialized = False  # Tracks if a HIGH state has been detected
current_channel = 0  # Start at channel 0

try:
    while True:
        # Read the current state of GPIO 23
        current_state = GPIO.input(23)

        # Detect the first HIGH to initialize
        if not initialized and current_state == GPIO.HIGH:
            initialized = True
            print("Initialized: Detected first HIGH state on GPIO 23")
        
        # Proceed only after initialization
        if initialized:
            # Detect a falling edge (HIGH to LOW transition)
            if last_state == GPIO.HIGH and current_state == GPIO.LOW:
                # Increment channel, wrap around after 128
                current_channel = (current_channel + 1) % 129
                switch_channel(current_channel)
            
            # Update last state
            last_state = current_state

        # Small delay to debounce
        time.sleep(0.05)

except KeyboardInterrupt:
    print("Exiting program...")

finally:
    # Clean up GPIO and close serial connection
    GPIO.cleanup()
    ser.close()
