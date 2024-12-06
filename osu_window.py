import mss
import cv2
import numpy as np
import time
import pygetwindow as gw
import multiprocessing


def get_osu_window_region():
    """
    Get the osu! window's location and size dynamically.
    """
    windows = gw.getWindowsWithTitle("osu!")
    if not windows:
        return None
    osu_window = windows[0]
    if not osu_window.isMaximized or not osu_window.isMinimized:
        return {
            "left": osu_window.left,
            "top": osu_window.top,
            "width": osu_window.width,
            "height": osu_window.height,
        }
    return None


def capture_screen(queue, refresh_rate=144):
    """
    Capture the osu! screen and send frames to the queue.
    """
    osu_region = get_osu_window_region()
    if not osu_region:
        print("osu! window not found. Exiting.")
        return

    interval = 1 / refresh_rate
    print(f"Starting screen capture at {refresh_rate}Hz")

    with mss.mss() as sct:
        while True:
            # Capture the screen
            screenshot = sct.grab(osu_region)
            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

            # Resize the frame for RL processing
            resized_frame = cv2.resize(frame, (160, 120))

            # Send the frame to the queue
            if not queue.full():
                queue.put(resized_frame)

            # Simulate frame delay
            time.sleep(interval)


if __name__ == "__main__":
    # Create a queue to share frames between processes
    frame_queue = multiprocessing.Queue(maxsize=10)

    # Start the screen capture process
    capture_process = multiprocessing.Process(
        target=capture_screen, args=(frame_queue, 144)
    )
    capture_process.start()

    # Display captured frames (for testing)
    while True:
        if not frame_queue.empty():
            frame = frame_queue.get()
            cv2.imshow("osu! Screen", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cv2.destroyAllWindows()
    capture_process.terminate()
    capture_process.join()
