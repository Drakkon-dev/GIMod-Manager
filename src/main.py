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

    def __start_launch_proccess__(self):
        subprocess.Popen(self.settings["AppPath"])
        subprocess.Popen(self.settings["GamePath"])

    # def __launch__(self, exe: str):
    #     try:
    #         subprocess.Popen(self.settings[
    #             "GamePath" if exe=="game" else (
    #                 "AppPath" if exe=="app" else ""
    #             )
    #         ])
    #     except FileNotFoundError:
    #         print(f"""Error: '{self.settings["GamePath" if exe=="game" else ("AppPath" if exe=="app" else "")]}' not found.""")
    #     except Exception as e:
    #         print(f"An error occurred: {str(e)}")
    #     if exe == "game":
    #         try:
    #             subprocess.Popen(self.settings['GamePath'])
    #         except FileNotFoundError:
    #             print(f"Error: '{self.settings['GamePath']}' not found.")
    #         except Exception as e:
    #             print(f"An error occurred: {str(e)}")
    #     elif exe == "app":
    #         try:
    #             subprocess.Popen(self.settings['AppPath'])
    #         except FileNotFoundError:
    #             print(f"Error: '{self.settings['AppPath']}' not found.")
    #         except Exception as e:
    #             print(f"An error occurred: {str(e)}")

    def __register_quit__(self):
        pygame.quit()
        sys.exit()

    def main(self):
        while True:
            self.screen.fill((255, 255, 255))
            mouse_pos = pygame.mouse.get_pos()
            mouse_buttons = pygame.mouse.get_pressed()
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.__register_quit__()
                self.ui_manager.process_events(event)
            
            
            
            self.ui_manager.update(1.0 / 60)
            self.ui_manager.draw_ui(self.screen)
            pygame.display.flip()

if __name__ == "__main__":
    app = App_launcher()
    app.main()