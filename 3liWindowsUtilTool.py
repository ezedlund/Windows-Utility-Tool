"""
      ___           ___              
     /  /\         /  /\       ___   
    /  /::\       /  /:/      /__/\  
   /  /:/\:\     /  /:/       \__\:\ 
  /  /::\ \:\   /  /:/        /  /::\
 /__/:/\:\ \:\ /__/:/      __/  /:/\/
 \  \:\ \:\_\/ \  \:\     /__/\/:/
  \  \:\ \:\    \  \:\    \  \::/    
   \  \:\_\/     \  \:\    \  \:\    
    \  \:\        \  \:\    \__\/    
     \__\/         \__\/     
        
Created by: Eli/jah
aka 3li
07/02/2023
https://github.com/ezedlund/Windows-Utility-Tool
"""


import os, sys, ctypes
from tkinter import *
from tkinter.ttk import *

VERSION = "v3.2"
# update made on 09/27/2023

# Dev settiong to hide/show console
# Leave it on True if you don't know what you're doing!
HIDE_CONSOLE = True


class MainGui(Tk):
    """
    MainGui(Tk)
    Main GUI class for 3liWindowsUtilTool
    """

    def __init__(self):
        # init
        Tk.__init__(self)
        self.geometry("300x250")
        self.configure(bg="#222222")
        self.title("Eli's Windows Util Tool")
        self.root = Frame(self)
        self.root.pack()

        # Toggles
        self.spotify_toggle = BooleanVar()
        self.discord_toggle = BooleanVar()
        self.auto_close_toggle = BooleanVar()

        # Create/Read options.txt
        try:
            if os.path.isfile(f"{os.getcwd()}\options.txt"):
                options_txt = []
                with open(f"{os.getcwd()}\options.txt", "r") as f:
                    for line in f:
                        line = line.replace("\n", "")
                        options_txt.append(line)
                if options_txt[0][len(options_txt[0]) - 4 :] == "True":
                    self.spotify_toggle = BooleanVar(value=True)
                if options_txt[1][len(options_txt[1]) - 4 :] == "True":
                    self.discord_toggle = BooleanVar(value=True)
                if options_txt[2][len(options_txt[2]) - 4 :] == "True":
                    self.auto_close_toggle = BooleanVar(value=True)
            else:
                default_options = [
                    "spotify_toggle: False",
                    "discord_toggle: False",
                    "auto_close_toggle: False",
                ]
                with open(f"{os.getcwd()}\options.txt", "w") as options_txt:
                    options_txt.write("\n".join(default_options))
            # options_txt = open("options.txt", "w")
        except Exception as err:
            print("Error with options.txt: " + str(err))

        # Style
        style = Style()
        style.theme_use("xpnative")
        style.configure("TFrame", background="#222222")
        style.configure(
            "TButton",
            font=("Hobo Std", 9, "bold"),
            foreground="black",
            background="#222222",
            borderwidth=1,
            focusthickness=1,
        )
        style.map(
            "TButton",
            background=[("active", "#222222")],
            foreground=[("active", "#222222")],
        )
        style.configure(
            "TLabel",
            font=("Hobo Std", 15, "bold"),
            background="#222222",
            foreground="#f5f5f5",
        )
        style.configure(
            "TCheckbutton",
            font=("Hobo Std", 10, "bold"),
            background="#222222",
            foreground="#f5f5f5",
        )
        # Objects #
        self.title = Label(
            self.root,
            text=f"Eli's Windows Util Tool {VERSION}",
        )
        self.welcome = Label(
            self.root,
            text=f"Welcome, {str(os.getlogin())}",
        )
        self.status = Label(self.root, text="Ready...")
        self.all_button = Button(
            self.root,
            text="Kill tasks!",
            command=lambda: self.all_killers(),
        )
        self.windows_button = Button(
            self.root,
            text="Kill windows tasks",
            command=lambda: self.random_win_killer(),
        )
        self.games_button = Button(
            self.root,
            text="Kill game tasks",
            command=lambda: self.assorted_games_killer(),
        )
        self.other_button = Button(
            self.root, text="More options", command=lambda: self.draw_other()
        )
        self.quit_button = Button(
            self.root,
            text="Quit",
            command=lambda: exit(),
        )
        self.main_menu_button = Button(
            self.root,
            text="Main Menu",
            command=lambda: self.draw_main(),
        )
        self.export_tasks_button = Button(
            self.root, text="Export tasks", command=lambda: self.export_tasks()
        )
        self.control_panel_button = Button(
            self.root,
            text="Control panel",
            command=lambda: self.control_panel(),
        )

        # Spacer
        self.spacer = Label(self.root, text="")

        # Toggles
        self.spotify_checkbox = Checkbutton(
            self.root,
            text="Kill Spotify",
            variable=self.spotify_toggle,
            onvalue=True,
            offvalue=False,
            command=lambda: self.save_options(),
        )
        self.discord_checkbox = Checkbutton(
            self.root,
            text="Kill Discord",
            variable=self.discord_toggle,
            onvalue=True,
            offvalue=False,
            command=lambda: self.save_options(),
        )
        self.auto_close_checkbox = Checkbutton(
            self.root,
            text="Close after clean",
            variable=self.auto_close_toggle,
            onvalue=True,
            offvalue=False,
            command=lambda: self.save_options(),
        )
        # draw main menu gui
        self.draw_main()

    def update_status(self, txt):
        """
        update_status(self, txt)
        txt -> text to set to status label
        * status label
        """
        self.status.config(text=f"{txt}")
        self.update()

    def draw_other(self):
        """
        draw_other(self)
        * other menu
        """
        self.clear_gui()
        # other buttons
        self.windows_button.grid(row=3, column=0, columnspan=2)
        self.games_button.grid(row=4, column=0, columnspan=2)
        self.export_tasks_button.grid(row=5, column=0, columnspan=2)
        self.control_panel_button.grid(row=6, column=0, columnspan=2)
        self.main_menu_button.grid(row=7, column=0, columnspan=2)
        self.spacer.grid(row=8, column=0)
        self.status.grid(row=9, column=0, columnspan=2)
        self.update_status("Ready...")

    def clear_gui(self):
        """
        clear_gui(self)
        * grid_remove everything but title, welcome, and status
        """
        self.all_button.grid_remove()
        self.windows_button.grid_remove()
        self.games_button.grid_remove()
        self.quit_button.grid_remove()
        self.status.grid_remove()
        self.other_button.grid_remove()
        self.main_menu_button.grid_remove()
        self.export_tasks_button.grid_remove()
        self.spotify_checkbox.grid_remove()
        self.discord_checkbox.grid_remove()
        self.control_panel_button.grid_remove()
        self.auto_close_checkbox.grid_remove()
        self.update_status("")
        self.update()

    def draw_main(self):
        """
        draw_main(self)
        * draw the main menu
        """
        self.clear_gui()
        self.spacer.grid(row=0, column=0)
        self.title.grid(row=1, column=0, columnspan=2)
        self.welcome.grid(row=2, column=0, columnspan=2)
        self.all_button.grid(row=3, column=0, columnspan=2)
        self.other_button.grid(row=4, column=0, columnspan=2)
        self.quit_button.grid(row=5, column=0, columnspan=2)
        self.spotify_checkbox.grid(row=6, column=0, columnspan=2)
        self.discord_checkbox.grid(row=7, column=0, columnspan=2)
        self.auto_close_checkbox.grid(row=8, column=0, columnspan=2)
        self.status.configure(font=("Hobo Std", 10, "bold"))
        self.spacer.grid(row=9, column=0)
        self.status.grid(row=10, column=0, columnspan=2)
        self.update_status("Ready...")

    def kill_process(self, process_name):
        """
        kill_process(self, process_name)
        process_name -> name of process to kill ex: "Spotify.exe"
        * use os.system to kill task provided
        """
        os.system(f"taskkill /f /im {process_name}")
        self.update_status(f"Killed {process_name}...")

    def random_win_killer(self, using_all=False):
        """
        random_win_killer(self, using_all=False)
        * kills some dumb tasks from windows
        """
        if not using_all:
            self.update_status("Cleaning windows...")
        windows_processes = [
            "CompatTelRunner.exe",
            "PhoneExperienceHost.exe",
            "yourphoneserver.exe",
            "yourphone.exe",
            "mysqld.exe",
            "msedge.exe",
        ]
        xbox_processes = [
            "xboxappservices.exe",
            "gamebarpresencewriter.exe",
            "gamebarftserver.exe",
            "gamebar.exe",
            "xboxapp.exe",
            "XboxIdp.exe",
            "XboxPCApp.exe",
            "gamingservices.exe",
            "gamingservicesnet.exe",
            "gameinputsvc.exe",
            "mysqld.exe",
            "XboxPcAppFT.exe",
        ]
        try:
            # Windows
            for process in windows_processes:
                self.kill_process(process)
            # Xbox
            for process in xbox_processes:
                self.kill_process(process)
            # Spotify and/or Discord
            if self.spotify_toggle.get():
                self.kill_process("Spotify.exe")
            if self.discord_toggle.get():
                self.kill_process("Discord.exe")
        except Exception as err:
            print(err)
            self.update_status("An error occured...")
        finally:
            if not using_all:
                self.update_status("Finished cleaning windows... \N{heavy check mark}")

    def assorted_games_killer(self, using_all=False):
        """
        assorted_games_killer(self, using_all=False)
        using_all -> flag for using clean all. doesnt show update_status
        * kills random leftover tasks from games
        """
        if not using_all:
            self.update_status("Cleaning games...")
        oculus_processes = [
            "OculusClient.exe",
            "OVRRedir.exe",
            "OVRServer_x64.exe",
            "OVRServiceLauncher.exe",
        ]
        ubisoft_processes = [
            "upc.exe",
            "UplayWebCore.exe",
            "UbisoftGameLauncher.exe",
            "UbisoftGameLauncher64.exe",
        ]
        other_processes = [
            "Agent.exe",
            "Battle.net.exe",
            "EpicWebHelper.exe",
            "EpicGamesLauncher.exe",
            "BsgLauncher.exe",
            "EADesktop.exe",
            "EABackgroundService.exe",
        ]
        riot_processes = ["RiotClientCrashHandler.exe", "RiotClientServices.exe"]
        try:
            # Oculus
            for process in oculus_processes:
                self.kill_process(process)
            # Ubisoft
            for process in ubisoft_processes:
                self.kill_process(process)
            # Riot
            for process in riot_processes:
                self.kill_process(process)
            # Other
            for process in other_processes:
                self.kill_process(process)
        except Exception as err:
            print(err)
            self.update_status("An error occured...")
        finally:
            if not using_all:
                self.update_status("Finished cleaning games... \N{heavy check mark}")

    def all_killers(self):
        """
        all_killers(self)
        * calls all killers
        """
        self.update_status("Cleaing all...")
        self.assorted_games_killer(True)
        self.random_win_killer(True)
        self.update_status("Finished cleaning all... \N{heavy check mark}")
        if self.auto_close_toggle.get() == True:
            self.update_status("Thanks!")
            quit()

    def export_tasks(self):
        """
        export_tasks(self)
        * save current task to txt
        """
        try:
            path = os.getcwd()
            with open("tasks.txt", "w") as f:
                for line in os.popen("tasklist").readlines():
                    f.write(line)
            os.startfile(path)
            self.update_status("Tasks exported... \N{heavy check mark}")
        except Exception as err:
            print(err)
            self.update_status("An error occured...")

    def control_panel(self):
        """
        control_panel(self)
        * show control panel
        """
        try:
            os.system("control panel")
            self.update_status("Opened control panel... \N{heavy check mark}")
        except Exception as err:
            print(err)
            self.update_status("An error occured...")

    def save_options(self):
        """
        save_options(self)
        * save options to txt
        """
        try:
            # check if file exists
            if os.path.isfile(f"{os.getcwd()}\options.txt"):
                # write current options
                options_txt = [
                    f"spotify_toggle: {self.spotify_toggle.get()}",
                    f"discord_toggle: {self.discord_toggle.get()}",
                    f"auto_close_toggle: {self.auto_close_toggle.get()}",
                ]
                with open(f"{os.getcwd()}\options.txt", "w") as f:
                    f.write("\n".join(options_txt))
            # file doesnt exist
            else:
                default_options = [
                    "spotify_toggle: False",
                    "discord_toggle: False",
                    "auto_close_toggle: False",
                ]
                with open(f"{os.getcwd()}\options.txt", "w") as options_txt:
                    options_txt.write("\n".join(default_options))
        except Exception as err:
            print(err)
            self.update_status("An error occured...")


if __name__ == "__main__":
    # Check admin
    if ctypes.windll.shell32.IsUserAnAdmin():
        # hide console
        if HIDE_CONSOLE:
            kernel32 = ctypes.WinDLL("kernel32")
            user32 = ctypes.WinDLL("user32")
            hWnd = kernel32.GetConsoleWindow()
            user32.ShowWindow(hWnd, 0)
        # launch GUI
        app = MainGui()
        app.mainloop()
    else:
        # re-launch as admin
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
