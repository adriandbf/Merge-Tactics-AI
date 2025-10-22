import pyautogui
import time

time.sleep(5)
x,y = pyautogui.position()
print(x)
print(y)

color= pyautogui.pixel(x,y)
print(color)