from env import MergeTacticsEnv
from agent import DQNAgent
import numpy as np

env = MergeTacticsEnv()
agent = DQNAgent(env.state_size, env.action_size)

state = env.reset()

for step in range(1):
    action = agent.act(state)
    next_state, reward, done = env.step(action)
    agent.remember(state, action, reward, next_state, done)
    print(f"Step {step+1}: action={action}, reward={reward}")
    state = next_state

# import os
# import pyautogui
# from actions import Actions

# def main():
#     a = Actions()

#     # Define a folder to save screenshots
#     out_dir = os.path.join(a.script_dir, "screenshots")
#     os.makedirs(out_dir, exist_ok=True)

#     # Define your current region settings (Mac only)
#     region = (
#         a.ELIXIR_X,
#         a.ELIXIR_Y,
#         a.ELIXIR_WIDTH,
#         a.ELIXIR_HEIGHT
#     )

#     print(f"[INFO] Capturing elixir region: {region}")

#     # Capture just the elixir bar region
#     screenshot = pyautogui.screenshot(region=region)

#     # Save for inspection
#     out_path = os.path.join(out_dir, "elixir_region_test.png")
#     screenshot.save(out_path)

#     print(f"[SUCCESS] Saved elixir region test image → {out_path}")
#     print("[INFO] Open that image and verify it contains ONLY the elixir bar area.")

# if __name__ == "__main__":
#     main()

# import cv2
# import numpy as np
# import os
# from PIL import ImageGrab
# from actions import Actions

# def main():
#     a = Actions()

#     region = (
#         a.ELIXIR_X,
#         a.ELIXIR_Y,
#         a.ELIXIR_X + a.ELIXIR_WIDTH,
#         a.ELIXIR_Y + a.ELIXIR_HEIGHT
#     )

#     # Capture the region currently used by count_elixir()
#     screenshot = ImageGrab.grab(bbox=region)
#     screen_rgb = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

#     # Save the raw capture for manual comparison
#     cv2.imwrite("screenshots/elixir_live_view.png", screen_rgb)
#     print("[INFO] Saved current elixir bar as screenshots/elixir_live_view.png")

#     # Compare with each template
#     images_folder = a.images_folder
#     for i in range(6):
#         template_path = os.path.join(images_folder, f"{i}elixir.png")
#         if not os.path.exists(template_path):
#             print(f"[WARN] Missing template: {template_path}")
#             continue

#         template = cv2.imread(template_path, cv2.IMREAD_COLOR)
#         res = cv2.matchTemplate(screen_rgb, template, cv2.TM_CCOEFF_NORMED)

#         _, max_val, _, _ = cv2.minMaxLoc(res)
#         print(f"[DEBUG] Match for {i}elixir.png → confidence={max_val:.3f}")

#     print("\n✅ Open screenshots/elixir_live_view.png and one of your templates side by side.")
#     print("They MUST be identical in scale, brightness, and color tone for template matching to work.")

# if __name__ == "__main__":
#     main()

