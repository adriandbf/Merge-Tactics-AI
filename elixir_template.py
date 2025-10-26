# Template for elixir counter
import os, time, pyautogui
from actions import Actions

a = Actions()
region = (a.ELIXIR_X, a.ELIXIR_Y, a.ELIXIR_WIDTH, a.ELIXIR_HEIGHT)
out = f"main_images"

for i in range(6):
    input(f"Set elixir={i}, then press ENTER...")
    shot = pyautogui.screenshot(region=region)
    shot.save(os.path.join(out, f"{i}elixir.png"))
    time.sleep(0.5)
