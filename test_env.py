from env import MergeTacticsEnv
import numpy as np

def main():
    env = MergeTacticsEnv()
    state = env.reset()
    print("Initial state:", state)

    for step in range(3):
        action = np.random.randint(0, env.action_size)
        next_state, reward, done = env.step(action)
        print(f"Step {step+1}: action={action}, reward={reward}, done={done}")
        print("Next state:", next_state)

if __name__ == "__main__":
    main()
