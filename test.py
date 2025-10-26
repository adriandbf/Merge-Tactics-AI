# from env import MergeTacticsEnv
# from agent import DQNAgent
# import numpy as np

# agentType = "DQN" # PPO or DQN available
# selfDefensePriority = 1 # number between 0 and 1
# randomPlay = False # True or False

# env = MergeTacticsEnv()
# env.set_selfDefensePriority(selfDefensePriority)
# env.set_constant_reward(randomPlay)
# if agentType == "DQN":
#     agent = DQNAgent(env.state_size, env.action_size)
# elif agentType == "PPO":
#     # to do: implement PPO case
#     pass
# else: 
#     agent = DQNAgent(env.state_size, env.action_size)

# done = False
# state = env.reset()


# for step in range(3):
    
#     if done == True:
#        state = env.reset()

#     action = agent.act(state)
#     next_state, reward, done = env.step(action)
#     agent.remember(state, action, reward, next_state, done)
#     print(f"Step {step+1}: action={action}, reward={reward}")
#     state = next_state


      
    

# import pyautogui
# import time

# time.sleep(5)
# x,y = pyautogui.position()
# print(x)
# print(y)

# color= pyautogui.pixel(x,y)
# print(color)

# # for mac the x and y need to be doubled - retina display makes it wonky
# color= pyautogui.pixel(2*x,2*y)
# print(color)
# from inference_sdk import InferenceHTTPClient

# client = InferenceHTTPClient(
#     api_url="https://serverless.roboflow.com",
#     api_key="Ql9J5N8ZaQruGzkj3KF4"
# )


# # doesnt work with multiple card images in one png, have to split cards into 3 seperate pngs
# image_path = f"screenshots/card_1.png"
# result1 = client.run_workflow(
#     workspace_name="adriandbf",
#     workflow_id="carddetection",
#     images={
#         "image": image_path
#     },
#     use_cache=True # cache workflow definition for 15 minutes
# )

# image_path = f"screenshots/area.png"
# result2 = client.run_workflow(
#     workspace_name="adriandbf",
#     workflow_id="troopdetection",
#     images={
#         "image": image_path
#     },
#     use_cache=True # cache workflow definition for 15 minutes
# )

# preds1 = result1[0]["predictions"]["predictions"]
# preds2 = result2[0]["predictions"]["predictions"]

# for p in preds1:
#     print(p['class'])

# for p in preds2:
#     print(p['class'])


# # import os
# # import pyautogui
# # from actions import Actions

# # def main():
# #     a = Actions()

# #     # Define a folder to save screenshots
# #     out_dir = os.path.join(a.script_dir, "screenshots")
# #     os.makedirs(out_dir, exist_ok=True)

# #     # Define your current region settings (Mac only)
# #     region = (
# #         a.ELIXIR_X,
# #         a.ELIXIR_Y,
# #         a.ELIXIR_WIDTH,
# #         a.ELIXIR_HEIGHT
# #     )

# #     print(f"[INFO] Capturing elixir region: {region}")

# #     # Capture just the elixir bar region
# #     screenshot = pyautogui.screenshot(region=region)

# #     # Save for inspection
# #     out_path = os.path.join(out_dir, "elixir_region_test.png")
# #     screenshot.save(out_path)

# #     print(f"[SUCCESS] Saved elixir region test image → {out_path}")
# #     print("[INFO] Open that image and verify it contains ONLY the elixir bar area.")

# # if __name__ == "__main__":
# #     main()

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

# Tests workflows from roboflow
# from inference_sdk import InferenceHTTPClient

# client = InferenceHTTPClient(
#     api_url="https://serverless.roboflow.com",
#     api_key="Ql9J5N8ZaQruGzkj3KF4"
# )


# # doesnt work with multiple card images in one png, have to split cards into 3 seperate pngs
# image_path = f"screenshots/card_1.png"
# result1 = client.run_workflow(
#     workspace_name="adriandbf",
#     workflow_id="carddetection",
#     images={
#         "image": image_path
#     },
#     use_cache=True # cache workflow definition for 15 minutes
# )

# image_path = f"screenshots/area.png"
# result2 = client.run_workflow(
#     workspace_name="adriandbf",
#     workflow_id="troopdetection",
#     images={
#         "image": image_path
#     },
#     use_cache=True # cache workflow definition for 15 minutes
# )

# preds1 = result1[0]["predictions"]["predictions"]
# preds2 = result2[0]["predictions"]["predictions"]

# for p in preds1:
#     print(p['class'])

# for p in preds2:
#     print(p['class'])

# from actions import Actions

# a = Actions()

# rank = a.get_ranking()
# print(rank)

# this s just copied from main of env.py -> to do: transform into test

# # testing screen capture functions
# def main():

#     m = MergeTacticsEnv()

#     # old_state = np.array([5, 10, 10])
#     # new_state = np.array([7, 9, 11])

#     # m._compute_reward(old_state, new_state)

# from actions import Actions
# import pyautogui
# import time

# def test_detect_is_done_live():
#     print("[INFO] Starting detect_is_done live test...")
#     try:
#         a = Actions()
#         print("[INFO] Actions initialized successfully.")
#         print(f"[INFO] Checking pixel at ({a.IS_DONE_X}, {a.IS_DONE_y}) expecting color {a.IS_DONE_COLOUR}")
#     except Exception as e:
#         print(f"[ERROR] Failed to initialize Actions: {e}")
#         return

#     # Give you a few seconds to focus the game window
#     print("[INFO] You have 3 seconds to prepare your screen...")
#     time.sleep(3)

#     try:
#         # Read raw pixel color directly
#         pixel_color = pyautogui.pixel(a.IS_DONE_X, a.IS_DONE_y)
#         print(f"[DEBUG] Raw pixel color read from screen: {pixel_color}")

#         # Now call your detection logic
#         result = a.detect_is_done()
#         print(f"[RESULT] detect_is_done() returned: {result}")

#         if result:
#             print("[PASS] Detected expected color → Game likely finished.")
#         else:
#             print("[INFO] Color didn't match expected finish color.")
#     except Exception as e:
#         print(f"[ERROR] Pixel read or detect_is_done() failed: {e}")

# if __name__ == "__main__":
#     test_detect_is_done_live()

import pyautogui
import time

print("Hover your mouse over a unique pixel for each screen type to capture RGB values.\n")
for screen in ["home", "loading", "match", "finished"]:
    input(f"Press Enter when ready to capture color for {screen}...")
    x, y = pyautogui.position()
    color = pyautogui.pixel(2*x, 2*y)
    print(f"{screen} → Position: ({x}, {y}), Color: {color}")
    time.sleep(1)

# Testing Detect Game State
# import time
# from actions import Actions

# def main():
    
#     a = Actions()

#     print("[TEST] Starting detect_game_state test...")
#     print("Move to different game screens (home, loading, match, finished) when prompted.\n")

#     try:
#         for i in range(5):
#             state = a.detect_game_state()
#             print(f"[{i+1}] Detected game state → {state}")
#             time.sleep(2)

#     except KeyboardInterrupt:
#         print("\n[TEST] Interrupted by user.")

#     print("\n[TEST COMPLETE] If all detections matched your current screen, the function works correctly.")

# if __name__ == "__main__":
#     main()

# import time
# import pyautogui
# from actions import Actions  # adjust this import path if needed

# def test_capture_player_position():
#     """
#     Tests whether capture_current_player_position() correctly identifies
#     which healthbar belongs to the player (blue color at one of the X positions).
#     """
#     a = Actions()

#     print("\n=== Player Position Detection Test ===")
#     print("Move to a match screen where the health bars are visible.")
#     time.sleep(3)

#     # capture and print raw pixel colors first
#     coords = [
#         ("P1", a.HEALTHBAR_X_P1, a.HEALTHBAR_Y),
#         ("P2", a.HEALTHBAR_X_P2, a.HEALTHBAR_Y),
#         ("P3", a.HEALTHBAR_X_P3, a.HEALTHBAR_Y),
#         ("P4", a.HEALTHBAR_X_P4, a.HEALTHBAR_Y),
#     ]
#     for label, x, y in coords:
#         color = pyautogui.pixel(x, y)
#         print(f"{label} → ({x}, {y}) color = {color}")

#     detected_position = a.capture_current_player_position()
#     print(f"\n[RESULT] Detected current player position: {detected_position}")

#     # basic assertions
#     if 1 <= detected_position <= 4:
#         print("[PASS] Valid player position detected.")
#     else:
#         print("[FAIL] No valid position detected — default used.")

# if __name__ == "__main__":
#     test_capture_player_position()
