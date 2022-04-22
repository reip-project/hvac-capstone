import time
import reip
import serial
import numpy as np

class SHTC3(reip.Block):
    baudrate = 115200
    port = "/dev/tty.usbmodem0E22C4B41"

    def __init__(self, **kw):
        # This is a data source block (no inputs)
        super().__init__(n_inputs=0, **kw)

    def init(self):
        # Initialize the connection to sensing device
        self.dev = serial.Serial(port=self.port, baudrate=self.baudrate)

    def process(self, *xs, meta):
        # Acquire sensor reading (send "m and get "temp,hum")
        self.dev.write("m".encode())
        time.sleep(0.1)
        raw = []
        while self.dev.in_waiting:
            raw.append(self.dev.read(1).decode())
        msg = "".join(raw).strip()
        # Format the data as per REIP API
        f = [float(v) for v in msg.split(",")]
        data = np.array(f).reshape(1, -1)  # axis=0 is for time
        # Pass the data to the next block
        return [data], {"timestamp": time.time()}

    def finish(self):
        # Close the connection
        self.dev.close()
