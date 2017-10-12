import pygame
import subprocess
import json
from urllib import request as urllib
import traceback
import pexpect
import atexit
""" Add custom commands for google assistant
    If success there won't be feedback from google asssistant
    Anyways, CustomAssistant has a function called _feedback which can be used to play an audio feedback
"""


class CustomAssistant():
    def __init__(self, assistant):
        self.params = None
        self.arg = None
        self.command = None
        self.assistant = assistant
        self.playshell = pexpect.spawn("mpsyt")
        self.playing_music = False
        self.music_paused = False
        with open("config.json", "r") as f:
            self.config = json.load(f)
        pygame.mixer.init()
        pygame.mixer.music.load(self.config["audio_feedback"])
        with open("actions.json", "r") as f:
            self.actions = json.load(f)
    def clean(self):
        self.params = None
        self.arg = None
        self.command = None
    def _feedback(self):
        pygame.mixer.music.play()
    """Add sudo to parameters
    """
    def add_sudo(self, params, sudo):
        if sudo:
            self.params.insert(0, "sudo")
    """Run a command using parameters.
       If sudo==True sudo will be added as parameter.
       Example:
            Supposing self.params = ["google-chrome", "github.com"]
            run_command(sudo=True) will execute in console "sudo google-chrome github.com"
            run_command(sudo=False) will execute in console "google-chrome github.com"
    """
    def run_command(self, sudo=None):  # run params
        self.add_sudo(self.params, sudo)
        subprocess.Popen(self.params, shell=False)
    """Open in browser
    """
    def open_in_browser(self, sudo=None):  # run params
        self.params.insert(0, self.config["browser"])
        self.add_sudo(self.params, sudo)
        subprocess.Popen(self.params, shell=False)
    """Search for a frase using the search_query defined in config.json
    """
    def search_for(self, sudo=None):
        self.params.insert(0, self.config["browser"])
        self.params[1] = self.config["search_query"].format(urllib.quote(self.params[1]))
        self.add_sudo(self.params, sudo)
        subprocess.Popen(self.params, shell=False)
    """Break user's phrase in command and argument
    """
    def analice_text(self, text):
        for action in self.actions.keys():
            if action in text and text.index(action) == 0:
                self.command = action
                break
        self.arg = text.replace("{} ".format(self.command), "")

    def play_music(self, sudo=None):
        if self.params[0] == "" and self.music_paused:
            self.playshell.send(" ")
        else:
            self.playshell.sendline('/' + self.params[0])
            self.playshell.sendline("all")
            self.playshell.send(' ')
        self.playing_music = True
    def next_song(self, sudo=None):
        self.playshell.send('>')
        self.playshell.send(' ')
        self.playing_music = True

    def previous_song(self, sudo=None):
        self.playshell.send('<')
        self.playshell.send(' ')
        self.playing_music = True

    def stop_music(self, sudo=None):
        if self.playing_music:
            self.playing_music = False
            self.music_paused = True
    def before_do(self):
        if self.playing_music:
            self.playshell.send(' ')
    def after_do(self):
        if self.playing_music and not self.music_paused:
            self.playshell.send(' ')
    """Call the right function with parameters according to what user said.
    """
    def process(self, event):
        self.analice_text(event.args["text"].lower())
        if self.command in self.actions.keys():
            action = self.actions[self.command]
            if "redirect_to" in action:
                action = self.actions[action["redirect_to"]]
            try:
                if "args" in action:
                    self.params = action["args"]
                else:
                    self.params = [self.arg]
                self.__getattribute__(action["action"])(action["sudo"])
                self.clean()
                self.assistant.stop_conversation()
                self._feedback()
                print("CUSTOM ACTION")
            except:
                traceback.print_exc()
    def exit(self):
        self.playshell.close()
    def at_exit(self):
        atexit.register(self)
