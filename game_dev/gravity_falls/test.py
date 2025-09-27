import time
import pyfirmata2
import pyautogui
import keyboard
import sys

# Replace 'COM5' with your Arduino's port (e.g., 'COM3' on Windows or '/dev/ttyACM0' on Linux/Mac)
board = pyfirmata2.Arduino('COM5')

# Set pin 3 to servo mode (this may be done automatically when using "d:3:s")
servo_pin_x = board.get_pin("d:3:s")
servo_pin_y = board.get_pin("d:6:s")

servo_pin_y.write(90)
servo_pin_x.write(90)

pyautogui.moveTo(pyautogui.size().width/2, pyautogui.size().height/2, 0)
start = pyautogui.position()

factor = [180 / pyautogui.size().width, 180 / pyautogui.size().height]
try:
    while True:
        now = pyautogui.position()
        x = 90 - (now[0] - start[0])*factor[0]
        y = 90 - (now[1] - start[1])*factor[1]
        
        if isinstance(servo_pin_y, pyfirmata2.pyfirmata2.Pin):
            try:
                servo_pin_y.write(y)
                servo_pin_x.write(x)
            except:
                print("unable")
                pyautogui.moveTo(pyautogui.size().width/2, pyautogui.size().height/2, 0)
                servo_pin_y.write(90)
                servo_pin_x.write(90)
        if keyboard.is_pressed("e"):
            sys.exit()
    
except KeyboardInterrupt:
    pass
