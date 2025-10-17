from env import MergeTacticsEnv
from agent import DQNAgent
import numpy as np

env = MergeTacticsEnv()
agent = DQNAgent(env.state_size, env.action_size)

state = env.reset()

for step in range(5):
    action = agent.act(state)
    next_state, reward, done = env.step(action)
    agent.remember(state, action, reward, next_state, done)
    print(f"Step {step+1}: action={action}, reward={reward}")
    state = next_state
