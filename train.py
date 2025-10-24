# Training of an agent
# till now: almost only copy and paste from https://github.com/krazyness/CRBot-public/blob/main/env.py

#? start state

import os
import torch
import glob
import json
from env import MergeTacticsEnv
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

# accepted inputs for agentType:  DQN or PPO  (default for invalid values is DQN)
# randomPlay is a flag if the agent should just play random or if it should actualy learn (sets a constant reward function)
# selfDefensePriority is a value between 0 and 1 that indicates how much defending our own health is rewarded with respect to decreasing the health of the others
def train(agentType, selfDefensePriority=1, randomPlay=False):

    env = MergeTacticsEnv()
    env.set_selfDefensePriority(selfDefensePriority)
    env.set_constant_reward(randomPlay)

    if agentType == "DQN":
        agent = DQNAgent(env.state_size, env.action_size)
    elif agentType == "PPO":
        # to do: implement PPO case
        pass
    else: 
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

    # data tracking
    metrics_path = os.path.join("models", "training_metrics.json")
    if os.path.exists(metrics_path):
        try:
            with open(metrics_path, "r") as f:
                metrics = json.load(f)
        except Exception:
            metrics = []
    else:
        metrics = []

    try:
        for ep in range(episodes):
            if controller.is_exit_requested():
                print("Training interrupted by user.")
                break

            state = env.reset()
            total_reward = 0

            print(f"Episode {ep + 1} starting. Epsilon: {agent.epsilon:.3f}") 
            
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

            # appending the data
            metrics.append({
                "episode": ep + 1,
                "total_reward": total_reward,
                "epsilon": round(agent.epsilon, 4),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

            # Save model and epsilon every 10 episodes
            if ep % 10 == 0:
                # update the values in the target model with those from the model we are training on
                agent.update_target_model()
                
                # save model 
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                model_path = os.path.join("models", f"model_{timestamp}.pth")
                torch.save(agent.model.state_dict(), model_path)

                # save epsilon value as meta data
                meta_path = os.path.join("models", f"meta_{timestamp}.json")
                with open(meta_path, "w") as f:
                    json.dump({"epsilon": agent.epsilon}, f)

                # saving metrics
                with open(metrics_path, "w") as f:
                    json.dump(metrics, f, indent=4)
                    
                print(f"Model and epsilon saved: {model_path}")
    except KeyboardInterrupt:
        print("\n[INTERRUPT] Ctrl+C detected — saving current progress...")

    finally:
        # Final save on exit
        agent.update_target_model()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_path = os.path.join("models", f"model_{timestamp}.pth")
        torch.save(agent.model.state_dict(), model_path)

        meta_path = os.path.join("models", f"meta_{timestamp}.json")
        with open(meta_path, "w") as f:
            json.dump({"epsilon": agent.epsilon}, f)

        with open(metrics_path, "w") as f:
            json.dump(metrics, f, indent=4)

        print(f"[FINAL SAVE] Model and metrics saved safely at {model_path}")

if __name__ == "__main__":
    
    agentType = input("Which agent would you like to train? (DQN / PPO) DQN will be trained if input invalid: ").strip().upper()

    if agentType == "DQN":
        train("DQN")
    elif agentType == "PPO":
        train("PPO")
    else:
        train("DQN")
        