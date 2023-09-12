
#! NO COMMENTS, SINCE THIS REPO IS NOT MEANT FOR COMMITS, but you can make a public repo if you want,
#! I don't think I will be activly supporting this, so I recommend you make one so others can make
#! improvements to the code, which would be much better than my own code currently.

import constants as Constants

import json
import contextlib
import win32gui
import win32api
import win32console
import sys
import os
import psutil
import re
import pyautogui
import pygetwindow as pgw

@contextlib.contextmanager
def suppress_output():
    with open(os.devnull, 'w') as fnull:
        old_stdout = sys.stdout
        sys.stdout = fnull
        try:
            yield
        finally:
            sys.stdout = old_stdout
with suppress_output():
    import pygame

class App:
    def __init__(self):
        pygame.init()
        self.settings_path = "settings.json"
        self.version = "0.1"
        self.console_hwnd = 0
        try:
            with open(self.settings_path, "r") as json_data:
                json_file_data = re.sub(r'//.*', '', json_data.read())
                self.settings_data = json.loads(json_file_data)
        except FileNotFoundError:
            print(f"Error: Settings file not found")
            self.__register_quit__()
        if not os.path.exists(self.settings_data["3DmigotoPath"]):
            print(f"Error: 3DMigoto directory not found")
            #self.__register_quit__()
        else:
            pass
        self.window_size = [1, 1]
        self.window_position = [0, 0]
        self.flags = pygame.NOFRAME | pygame.SRCALPHA
        self.screen = pygame.display.set_mode(self.window_size, self.flags)
        pygame.display.set_caption(self.settings_data["AppTitle"])
        self.hwnd = pygame.display.get_wm_info()["window"]
        self.__pygame_window_thing__()
        self.__hide_window__(True)

    def __pygame_window_thing__(self):
        win32gui.SetWindowPos(self.hwnd, Constants.HWND_TOPMOST, 0, 0, 0, 0, Constants.SWP_NOMOVE | Constants.SWP_NOSIZE)
        win32gui.SetWindowLong(self.hwnd, Constants.GWL_EXSTYLE, Constants.WS_EX_NOACTIVATE | Constants.WS_EX_LAYERED)
        win32gui.SetLayeredWindowAttributes(self.hwnd, win32api.RGB(255, 0, 128), 0, Constants.LWA_COLORKEY)

    def __register_quit__(self):
        pygame.quit()
        sys.exit()
    def __get_display_pixel_color__(self, x: int, y: int) -> tuple[int, int, int]:
        screenshot = pyautogui.screenshot(region=(x, y, 1, 1))
        return screenshot.getpixel((0, 0))
    def __is_game_pause_menu_open__(self):
        return True
    def __is_game_focused__(self) -> bool:
        try:
            window = pgw.getWindowsWithTitle(self.settings_data["GameName"])
            if window:
                return window[0].isActive
            else:
                return False
        except pgw.PyGetWindowException:
            return False
    def __is_game_windowed__(self) -> bool:
        window = pgw.getWindowsWithTitle(self.settings_data["GameName"])
        if window:
            window = window[0]
            window_size = window.size
            screen_size = pyautogui.size()
            if window_size == screen_size:
                return False
            else:
                return True
        else:
            print(f"No window found with the title '{self.settings_data['GameName']}'.")
            self.__register_quit__()
    def __get_game_window_size__(self) -> list[int, int]:
        try:
            window = pgw.getWindowsWithTitle(self.settings_data["GameName"])
            if window:
                width, height = window[0].size
                return [width, height]
            else:
                return [0, 0]
        except pgw.PyGetWindowException:
            return [0, 0]
    def __get_game_window_position__(self) -> list[int, int]:
        try:
            window = pgw.getWindowsWithTitle(self.settings_data["GameName"])
            if window:
                x, y = window[0].left, window[0].top
                return [x, y]
            else:
                return [0, 0]
        except pgw.PyGetWindowException:
            return [0, 0]
    def __is_game_process_running__(self) -> bool:
        for proc in psutil.process_iter():
            try:
                if proc.name() == self.settings_data["AnimeGamePROC"]:
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                return False
    def __set_window_size__(self, width: int, height: int):
        self.window_size = [round(width), round(height)]
        pygame.display.set_mode(self.window_size, self.flags)
        self.__pygame_window_thing__()
    def __set_window_position__(self, x: int, y: int):
        self.window_position = [round(x), round(y)]
        self.__window_set__()
    def __window_set__(self):
        win32gui.SetWindowPos(self.hwnd, 0, round(self.window_position[0]), round(self.window_position[1]), 0, 0, Constants.SWP_NOSIZE)
    def __hide_window__(self, hide: bool):
        if hide:win32gui.ShowWindow(self.hwnd, Constants.SW_HIDE)
        else:win32gui.ShowWindow(self.hwnd, Constants.SW_SHOWNA)

    def main(self):
        found_game_proc: bool = False
        print(f"""
---------------------------------- Genshin Migoto Mod Manager ----------------------------------

Mod-Manager Version: {self.version}
Looking for PROC: {self.settings_data['AnimeGamePROC']}

""")
        self.console_hwnd = win32console.GetConsoleWindow()
        while True:
            if found_game_proc:
                break
            for proc in psutil.process_iter():
                try:
                    if proc.name() == self.settings_data["AnimeGamePROC"]:
                        print("Found Genshin Impact")
                        print(proc.name(), proc.pid)
                        found_game_proc = True
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
        if found_game_proc:
            self.__main__()

    def __main__(self):
        prev_game_window_size: list[int, int] = self.__get_game_window_size__()
        prev_game_window_position: list[int, int] = self.__get_game_window_position__()
        self.__set_window_size__(
            prev_game_window_size[0] * (self.settings_data["SizeRelative"][0]/100),
            prev_game_window_size[1] * (self.settings_data["SizeRelative"][1]/100)
        )
        self.__set_window_position__(
            prev_game_window_position[0] + (prev_game_window_size[0]*(self.settings_data["PostionRelative"][0])),
            prev_game_window_position[1] + (prev_game_window_size[1]*(self.settings_data["PostionRelative"][1]))
        )
        if not self.settings_data["Debug"]:
                win32gui.ShowWindow(self.console_hwnd, Constants.SW_HIDE)
        while True:
            #os.system('cls' if os.name == 'nt' else 'clear')
            self.screen.fill((255, 0, 128))
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT or not self.__is_game_focused__():
                    if not self.__is_game_process_running__():
                        self.__register_quit__()
            
            if self.__is_game_focused__():
                game_window_size = self.__get_game_window_size__()
                game_window_position = self.__get_game_window_position__()
                if (game_window_size != prev_game_window_size) or (game_window_position != prev_game_window_position):
                    print(f"{self.window_size}")
                    self.__set_window_size__(
                        game_window_size[0] * (self.settings_data["SizeRelative"][0]/100),
                        game_window_size[1] * (self.settings_data["SizeRelative"][1]/100)
                    )
                    self.__set_window_position__(
                        game_window_position[0] + (game_window_size[0]*(self.settings_data["PostionRelative"][0]/100)),
                        game_window_position[1] + (game_window_size[1]*(self.settings_data["PostionRelative"][1]/100))
                    )
            self.__hide_window__(
                False if self.__is_game_focused__() and self.__is_game_pause_menu_open__() 
                else True
            )
            
            pygame.draw.circle(self.screen, (0, 0, 0), (250, 250), 200)
            pygame.draw.circle(self.screen, (255, 0, 128), (250, 250), 20)
            
            
            pygame.display.flip()
            prev_game_window_size = self.__get_game_window_size__()
            prev_game_window_position = self.__get_game_window_position__()

if __name__ == "__main__":
    print("Loading...")
    app = App()
    app.main()