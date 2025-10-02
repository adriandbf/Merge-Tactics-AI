# Training of an agent
# till now: almost only copy and paste from https://github.com/krazyness/CRBot-public/blob/main/env.py

import os
import torch
import glob
import json
from env import ClashRoyaleEnv
from agent import DQNAgent
from pynput import keyboard
from datetime import datetime

# keyboard controller to stop training in a save way (press q to stop the training)
class KeyboardController:
    def __init__(self):
        self.should_exit = False
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def on_press(self, key):
        try:
            if key.char == 'q':
                print("\nShutdown requested - cleaning up...")
                self.should_exit = True
        # just ignore if a special key is pressed which is not a char value
        except AttributeError:
            pass  # Special key pressed
            
    def is_exit_requested(self):
        return self.should_exit

# if there is at least one model already in the model folder, get the latest one
def get_latest_model_path(models_dir="models"):
    model_files = glob.glob(os.path.join(models_dir, "model_*.pth"))
    if not model_files:
        return None
    model_files.sort()  # Lexicographical sort works for timestamps
    return model_files[-1]

def train():
    
    env = ClashRoyaleEnv()
    agent = DQNAgent(env.state_size, env.action_size)

    # Ensure models directory exists
    os.makedirs("models", exist_ok=True)

    # Load latest model if available
    latest_model = get_latest_model_path("models")
    if latest_model:
        agent.load(os.path.basename(latest_model))
        # Load epsilon
        meta_path = latest_model.replace("model_", "meta_").replace(".pth", ".json")
        if os.path.exists(meta_path):
            with open(meta_path, "r") as f:
                meta = json.load(f)
                agent.epsilon = meta.get("epsilon", 1.0)
            print(f"Epsilon loaded: {agent.epsilon}")

    # to do: set constants for nicer manipulation of episodes batch size and so on 
    controller = KeyboardController()
    episodes = 10000
    batch_size = 32

    for ep in range(episodes):
        if controller.is_exit_requested():
            print("Training interrupted by user.")
            break

        state = env.reset()
        print(f"Episode {ep + 1} starting. Epsilon: {agent.epsilon:.3f}") 
        total_reward = 0
        done = False
        while not done:

            # get current action the model would do 
            action = agent.act(state)
            # perform the action and save the outcome
            next_state, reward, done = env.step(action)
            agent.remember(state, action, reward, next_state, done)
            # update the model
            agent.replay(batch_size)
            # update vars
            state = next_state
            total_reward += reward
        print(f"Episode {ep + 1}: Total Reward = {total_reward:.2f}, Epsilon = {agent.epsilon:.3f}")

        # Save model and epsilon every 10 episodes
        if ep % 10 == 0:
            # update the values in the target model with those from the model we are training on
            agent.update_target_model()
            
            # save model 
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            model_path = os.path.join("models", f"model_{timestamp}.pth")
            torch.save(agent.model.state_dict(), model_path)

            # save epsilon value as meta data
            with open(os.path.join("models", f"meta_{timestamp}.json"), "w") as f:
                json.dump({"epsilon": agent.epsilon}, f)
            print(f"Model and epsilon saved to {model_path}")

if __name__ == "__main__":
    train()