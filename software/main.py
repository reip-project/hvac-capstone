# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import time
import reip

import serial
import numpy as np



def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

def demo():
    dev = serial.Serial(port="/dev/cu.usbmodem0E22C4B41", baudrate=115200)
    while True:
        cmd = input()
        if cmd == "exit":
            break
        dev.write(cmd.encode())
        time.sleep(0.1)
        raw = []
        while dev.in_waiting:
            raw.append(dev.read(1).decode())
        msg = "".join(raw).strip()
        # TODO: Parse two float values from msg
        print(msg)
    dev.close()





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print_hi('PyCharm')
    demo()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

