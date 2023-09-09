import pygame
from pygame_gui import UIManager
from pygame_gui.elements import UIButton
import ctypes
import pystray
from PIL import Image
import json
import sys
import win32gui
import os
import subprocess
import psutil

# NO COMMENTS, THIS IS NOT MEANT FOR PEOPLE TO COMMIT TO, but you can make a public repo if you wish, since I don't
# think that I will be actively contributing to this project, and yes I know my code is shit.

class App_launcher:
    def __init__(self):
        pygame.init()
        
        self.hide_launcher = False
        self.GWL_EXSTYLE = -20
        self.WS_EX_NOACTIVATE = 0x08000000
        self.run_once = 0
        
        try:
            with open("config.json", "r") as json_data:
                self.settings = json.load(json_data)
        except FileNotFoundError:
            print(f"Error: config file not found")
            with open("config.json", "w") as new_file:
                json.dump({
                    "Title": "Window Title",
                    "GameTitle": "Genshin Impact",
                    "WindowSize": [900, 600],
                    "IconPath": "assets/icon.ico",
                    "AppPath": "Path/to/App/app.exe",
                    "GamePath": "Path/to/Game/game.exe"
                }, new_file, indent = 4)
            self.__register_quit__()

        self.window_size = self.settings["WindowSize"]
        self.flags = pygame.SCALED
        self.screen = pygame.display.set_mode(self.window_size, self.flags)
        try:
            icon_image = Image.open(self.settings["IconPath"])
            self.icon = pygame.image.fromstring(icon_image.tobytes(), icon_image.size, icon_image.mode)
            pygame.display.set_icon(self.icon)
        except FileNotFoundError:
            print(f"Error: '{self.settings['IconPath']}' not found")
            self.__register_quit__()
        pygame.display.set_caption(self.settings["Title"])
        self.screen.fill((255, 255, 255))
        pygame.display.flip()
        self.hwnd = pygame.display.get_wm_info()["window"]
        self.ui_manager = UIManager(self.window_size)

        self.game_title = self.settings["GameTitle"]

    def __launch__(self, exe: str):
        try:
            subprocess.Popen(self.settings[
                "GamePath" if exe=="game" else (
                    "AppPath" if exe=="app" else ""
                )
            ])
        except FileNotFoundError:
            print(f"""Error: '{self.settings["GamePath" if exe=="game" else ("AppPath" if exe=="app" else "")]}' not found.""")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        # if exe == "game":
        #     try:
        #         subprocess.Popen(self.settings['GamePath'])
        #     except FileNotFoundError:
        #         print(f"Error: '{self.settings['GamePath']}' not found.")
        #     except Exception as e:
        #         print(f"An error occurred: {str(e)}")
        # elif exe == "app":
        #     try:
        #         subprocess.Popen(self.settings['AppPath'])
        #     except FileNotFoundError:
        #         print(f"Error: '{self.settings['AppPath']}' not found.")
        #     except Exception as e:
        #         print(f"An error occurred: {str(e)}")
    def __register_quit__(self):
        pygame.quit()
        sys.exit()
    def __is_anime_game_running__(self):
        focused_window_handle = win32gui.GetForegroundWindow()
        focused_window_title = win32gui.GetWindowText(focused_window_handle)
        return focused_window_title == self.game_title
    def __hide_or_show_window__(self):
        if self.hide_launcher:
            pygame.display.iconify()
            ctypes.windll.user32.SetWindowLongPtrW(self.hwnd, self.GWL_EXSTYLE, self.WS_EX_NOACTIVATE)
        elif not self.hide_launcher:
            ctypes.windll.user32.SetWindowLongPtrW(self.hwnd, self.GWL_EXSTYLE, 0)

    def main(self):
        while True:
            if self.__is_anime_game_running__() and self.run_once == 0:
                
                
                self.run_once += 1
            else:
                self.hide_launcher = False

            if not self.hide_launcher:
                self.screen.fill((255, 255, 255))
                mouse_pos = pygame.mouse.get_pos()
                mouse_buttons = pygame.mouse.get_pressed()
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        self.__register_quit__()
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        self.hide_launcher = True
                    self.ui_manager.process_events(event)

                self.ui_manager.update(1.0 / 60)
                self.ui_manager.draw_ui(self.screen)
                pygame.display.flip()

            self.__hide_or_show_window__()

if __name__ == "__main__":
    app = App_launcher()
    app.main()