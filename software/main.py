# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import time
import reip
import pandas as pd
import csv
import serial
import numpy as np



def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.



lst = []
def demo():
    dev = serial.Serial(port="/dev/tty.usbmodem0E22C4B41", baudrate=115200)
    #TODO Read any trash present
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
        a = msg.split(",")
        f = [float(v) for v in a]
        ar = np.array(f)
        dev2 = serial.Serial()
        print(a, type(a))
        print(ar, type(ar))
        name=['tem','humi']
        data1= pd.DataFrame(columns = name , data = [f] )
        print(data1)
        data1.to_csv('data1')
        #lst.append(a)
    dev.close()






# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print_hi('PyCharm')
    demo()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

