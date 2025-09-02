import digitalio
import board
import time

# Configure axon output (D15)
axon = digitalio.DigitalInOut(board.D15)
axon.direction = digitalio.Direction.OUTPUT
axon.value = True  # Start inactive (HIGH)

print("AXON TRANSMITTER TEST")
print("Pulsing D15 every 2 seconds")

try:
    while True:
        # Active LOW pulse
        axon.value = False
        print("AXON ON (LOW)")
        time.sleep(0.5)  # Pulse duration
        
        axon.value = True
        print("AXON OFF (HIGH)")
        time.sleep(1.5)  # Total period = 2 seconds
        
except KeyboardInterrupt:
    axon.value = True
    print("\nTransmitter stopped")