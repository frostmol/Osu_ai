import pygetwindow as gw
import pyautogui
import numpy as np
import cv2
import time

def find_osu_window():
    """
    Ищет окно osu! по названию
    """
    for window in gw.getAllTitles():
        if "osu!" in window:
            return gw.getWindowsWithTitle(window)[0]
    return None

def capture_osu_window(window):
    """
    Захватывает содержимое окна osu! и возвращает его как изображение
    """
    if not window:
        return None
    left, top, width, height = window.left, window.top, window.width, window.height
    screenshot = pyautogui.screenshot(region=(left, top, width, height))
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

def main():
    print("Ищу окно osu!...")
    osu_window = find_osu_window()
    if not osu_window:
        print("Окно osu! не найдено!")
        return

    print("Окно osu! найдено. Начинаю захват.")
    try:
        while True:
            # Захватываем изображение
            frame = capture_osu_window(osu_window)
            if frame is not None:
                # Показываем изображение в реальном времени
                cv2.imshow("osu! Capture", frame)

                # Если нажата клавиша Q, выход из программы
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                print("Ошибка захвата изображения.")
                break

            time.sleep(0.01)  # Небольшая задержка для оптимизации
    finally:
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
