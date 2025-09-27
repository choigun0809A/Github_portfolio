import time
import pyfirmata2
import keyboard
import sys

import pyfirmata2.util




board = pyfirmata2.Arduino('COM5')


waist = board.get_pin("d:3:s")
lower_arm = board.get_pin("d:4:s")
upper_arm = board.get_pin("d:5:s")
tip_arm = board.get_pin("d:6:s")
spinner = board.get_pin("d:7:s")
claw = board.get_pin("d:9:s")


waisto = 90
lower_armo = 90
upper_armo = 90
tip_armo = 90
spinnero = 90
clawo = 90

waist.write(waisto)
lower_arm.write(lower_armo)
upper_arm.write(upper_armo)
tip_arm.write(tip_armo)
claw.write(clawo)

speed = 2
while True:
    

    change = 0
    if keyboard.is_pressed("d"):
        change -= speed
    if keyboard.is_pressed("a"):
        change += speed

    waisto += change
    if waisto < 0 or waisto > 180:
        waisto -= change
    
    change = 0
    if keyboard.is_pressed("s"):
        change -= speed
    if keyboard.is_pressed("w"):
        change += speed
        
    lower_armo += change
    if lower_armo < 0 or lower_armo > 180:
        lower_armo -= change

        
    change = 0
    if keyboard.is_pressed("r"):
        change -= speed
    if keyboard.is_pressed("f"):
        change += speed
    

    upper_armo += change
    if upper_armo < 10 or upper_armo > 180:
        upper_armo -= change

    
    change = 0
    if keyboard.is_pressed("q"):
        change -= speed
    if keyboard.is_pressed("e"):
        change += speed
    

    tip_armo += change
    if tip_armo < 10 or tip_armo > 180:
        tip_armo -= change

    change = 0
    if keyboard.is_pressed("t"):
        change -= speed
    if keyboard.is_pressed("g"):
        change += speed
    

    spinnero += change
    if spinnero < 10 or spinnero > 180:
        spinnero -= change


    change = 0
    if keyboard.is_pressed("z"):
        change -= speed
    if keyboard.is_pressed("x"):
        change += speed
    

    clawo += change
    if clawo < 10 or clawo > 98:
        clawo -= change
    print(f"Waist: {waisto}, Lower Arm: {lower_armo}, Upper Arm: {upper_armo}, tip arm: {tip_armo}", f"spinner {spinnero}, claw: {clawo}")
    
    waist.write(waisto)
    upper_arm.write(upper_armo)
    lower_arm.write(lower_armo)
    tip_arm.write(tip_armo)
    claw.write(clawo)
    spinner.write(spinnero)

    time.sleep(0.05)

