import pyautogui
import time

time.sleep(5)
x,y = pyautogui.position()
print(x)
print(y)

# for mac the x and y need to be doubled - retina display makes it wonky
color= pyautogui.pixel(2*x,2*y)
print(color)

"""
1006
267
RGB(red=26, green=26, blue=32)

1084
139
1097
149

1211
139
1224
149

1340
139
1352
150

1466
138
1481
148


"""