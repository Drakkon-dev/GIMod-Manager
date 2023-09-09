import requests
from bs4 import BeautifulSoup
import json
import win32gui
import sys
import os
import psutil
import ctypes
import pyautogui
import pygame

class App:
    def __init__(self,
                 settings_path: str,
                ):
        pygame.init()

        with open(settings_path, "r") as json_data:
            self.settings_data = json.load(json_data)

        self.window_size = (self.settings_data["SizeRelative"][0], self.settings_data["SizeRelative"][1])
        self.screen = pygame.display.set_mode(self.window_size, pygame.NOFRAME)
        self.hwnd = pygame.display.get_wm_info()["window"]

        # I don't want the window to take focus so I used ctypes,
        # I should've just used a proper gui library instead of pygame
        GWL_EXSTYLE = -20
        WS_EX_NOACTIVATE = 0x08000000
        ctypes.windll.user32.SetWindowLongPtrW(self.hwnd, GWL_EXSTYLE, WS_EX_NOACTIVATE)

    def __get_display_pixel_color__(self, x: int, y: int):
        screenshot = pyautogui.screenshot()
        return screenshot.getpixel((x, y))

    def __is_window_focused__(self, window_title: str):
        focused_window_handle = win32gui.GetForegroundWindow()
        focused_window_title = win32gui.GetWindowText(focused_window_handle)
        return focused_window_title == window_title

    def main(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 2):
                    pygame.quit()
                    sys.exit()
            
            #os.system('cls' if os.name == 'nt' else 'clear')
            
            pygame.display.flip()

if __name__ == "__main__":
    app = App("src/settings.json")
    app.main()