import cv2
import time
import numpy as np
import pyautogui
from gym import Env, spaces
from multiprocessing import Queue


class OsuEnv(Env):
    def __init__(self, frame_queue, no_fail=True):
        super(OsuEnv, self).__init__()
        self.frame_queue = frame_queue
        self.no_fail = no_fail

        # Observation space: Captured screen frames (160x120 RGB)
        self.observation_space = spaces.Box(
            low=0, high=255, shape=(120, 160, 3), dtype=np.uint8
        )
        
        # Action space: Placeholder (you may adjust for specific actions)
        self.action_space = spaces.Discrete(4)  # Actions could be taps, holds, etc.

        # Initialize variables
        self.reward = 0
        self.done = False

    def reset(self):
        """
        Reset the environment by simulating key presses to start a new beatmap.
        """
        print("Resetting environment...")
        pyautogui.press("escape")  # Go back to map selection
        time.sleep(1)
        pyautogui.press("f2")  # Choose a random map
        time.sleep(1)
        pyautogui.press("enter")  # Start the map
        time.sleep(2)  # Wait for the map to start

        # Reset internal state
        self.reward = 0
        self.done = False

        # Return the initial observation
        return self._get_observation()

    def _get_observation(self):
        """
        Fetch the latest frame from the queue.
        """
        if not self.frame_queue.empty():
            return self.frame_queue.get()
        else:
            # Return a blank frame if no frames are available
            return np.zeros((120, 160, 3), dtype=np.uint8)

    def _calculate_reward(self, miss, hit50, hit100, hit300, combo, accuracy):
        """
        Calculate reward based on osu! scoring metrics.
        """
        base_reward = (300 * hit300 + 100 * hit100 + 50 * hit50 - 50 * miss)
        combo_bonus = combo * 0.1  # Example: Scale combo bonus
        accuracy_bonus = accuracy * 10  # Example: Scale accuracy bonus
        return base_reward + combo_bonus + accuracy_bonus

    def step(self, action):
        """
        Perform a step in the environment.
        """
        # Simulate frame delay
        time.sleep(1 / 144)

        # Capture observation
        observation = self._get_observation()

        # Placeholder: Extract game stats ( need to parse osu! memory or logs for this)
        miss, hit50, hit100, hit300, combo, accuracy = 0, 0, 0, 0, 1, 1.0  # Dummy values

        # Calculate reward
        reward = self._calculate_reward(miss, hit50, hit100, hit300, combo, accuracy)

        # Determine if the episode is done
        self.done = False  # Placeholder: Check actual game state
        
        return observation, reward, self.done, {}

    def render(self, mode="human"):
        """
        Optional: Display the current frame.
        """
        frame = self._get_observation()
        cv2.imshow("osu! Environment", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.close()

    def close(self):
        """
        Close the environment and cleanup.
        """
        cv2.destroyAllWindows()


if __name__ == "__main__":
    # Create a queue to receive frames from the screen capture process
    frame_queue = Queue(maxsize=10)

    # Assume the screen capture program is running separately and populating the queue
    env = OsuEnv(frame_queue=frame_queue, no_fail=True)
    obs = env.reset()

    for _ in range(1000):  # Run for a fixed number of steps
        action = env.action_space.sample()  # Placeholder for RL agent's action
        obs, reward, done, info = env.step(action)
        env.render()
        if done:
            obs = env.reset()

    env.close()
