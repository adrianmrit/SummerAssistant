import subprocess
import json
from urllib import request as urllib
import traceback
import pexpect
import atexit
from gtts import gTTS
import os
import re
""" Add custom commands for google assistant
    If success there won't be feedback from google asssistant
    Anyways, CustomAssistant has a function called _feedback which can be used to play an audio feedback
"""
import settings

class CustomAssistant():
    def __init__(self, assistant):
        self.action = None
        self.args = None
        self.function = None
        self.assistant = assistant
        self.playshell = pexpect.spawn("mpsyt")
        self.playing_music = False
        self.music_paused = False
        tts = gTTS(text=settings.wellcome_txt, lang='en')
        if os.path.isfile("responses/wellcome.mp3"):
            pass
        else:
            tts.save("responses/wellcome.mp3")
        with open("actions.json", "r") as f:
            self.actions = json.load(f)
        with open("dictionary.json", "r") as f:
            self.dictionary = json.load(f)
        subprocess.Popen(["mpv", "responses/wellcome.mp3"])
    def clean(self):
        self.args = None
        self.action = None
        self.function = None
    def _feedback(self):
        subprocess.Popen(["mpv", settings.audio_feedback], shell=False)
    """Run a command using parameters.
       If sudo==True sudo will be added as parameter.
       Example:
            Supposing self.params = ["google-chrome", "github.com"]
            run_command(sudo=True) will execute in console "sudo google-chrome github.com"
            run_command(sudo=False) will execute in console "google-chrome github.com"
    """
    def run_command(self):  # run params
        if "close" in self.args:
            if self.args["command"] == "google-chrome":
                self.args["command"] = "chrome"
            # subprocess.Popen(["killall", self.args["command"]], shell=False)
            subprocess.Popen("killall {}".format(self.args["command"]))
        else:
            # subprocess.Popen([self.args["command"]], shell=False)
            subprocess.Popen("gnome-terminal -e {}".format(self.args["command"]))
    """Open in browser
    """
    def open_in_browser(self):  # run params
        subprocess.Popen([settings.browser, self.args["url"]], shell=False)
    """Search for a frase using the search_query defined in config.json
    """
    def search_for(self):
        query = settings.search_query.format(urllib.quote(self.args["query"]))
        subprocess.Popen([settings.browser, query], shell=False)
    """Break user's phrase in command and argument
    """
    def analice_text(self, text):
        for action in self.actions.keys():
            regex = re.compile(action)
            m = regex.search(text)
            if m:
                self.action = self.actions[action]
                self.args = m.groupdict()
                for key in self.args.keys():
                    if key in self.dictionary:
                        for word in self.dictionary[key].keys():
                            if self.args[key] == word:
                                self.args[key] = self.dictionary[key][word]
                if "additional_args" in self.action:
                    for arg in self.action["additional_args"]:
                        self.args.update({arg:True})
                print(self.args)
                break

    def play_music(self):
        if not self.args["query"] in self.args and self.music_paused:
            self.playshell.send(" ")
            self.music_paused = False
        else:
            self.playshell.sendline('/' + self.args["query"])
            self.playshell.sendline("all")
        self.playshell.sendline(" ")
        self.playing_music = True
    def next_song(self):
        self.playshell.send('>')
        self.playshell.send(' ')
        self.playing_music = True

    def previous_song(self):
        self.playshell.send('<')
        self.playshell.send(' ')
        self.playing_music = True

    def stop_music(self):
        if self.playing_music:
            self.playing_music = False
            self.music_paused = True
    def before_do(self):
        if self.playing_music and not self.music_paused:
            self.playshell.send(' ')
    def after_do(self):
        if self.playing_music and not self.music_paused:
            self.playshell.send(' ')
    """Call the right function with parameters according to what user said.
    """
    def play_response(self, event, cache=True, error=False):
        if error:
            for key in self.args.keys():
                try:
                    self.action["response_error"] = self.action["response_error"].replace("<{key}>".format(key=key), self.args[key])
                except TypeError:
                    pass
            tts = gTTS(text=self.action["response_error"], lang='en')
            file_name = "responses/{file_name}_error.mp3".format(file_name=event.args["text"].lower().replace(" ", "_"))
        else:
            for key in self.args.keys():
                try:
                    self.action["response_success"] = self.action["response_success"].replace("<{key}>".format(key=key), self.args[key])
                except TypeError:
                    pass
            tts = gTTS(text=self.action["response_success"], lang='en')
            file_name = "responses/{file_name}.mp3".format(file_name=event.args["text"].lower().replace(" ", "_"))
        if cache:
            if os.path.isfile(file_name):
                pass
            else:
                tts.save(file_name)
            subprocess.Popen(["mpv", file_name], shell=False)
        else:
            tts.save(file_name)
            subprocess.Popen(["mpv", file_name], shell=False)
            os.remove(file_name)
    def no_action(self):
        pass
    def process(self, event):
        self.analice_text(event.args["text"].lower())
        try:
            self.__getattribute__(self.action["action"])()
            self.assistant.stop_conversation()
            if self.action and "response_success" in self.action:
                if  self.action["cache_response"]:
                    cache = True
                else:
                    cache = False
                self.play_response(event, cache=cache)
            else:
                self._feedback()
            self.clean()
            print("CUSTOM ACTION")
        except:
            if self.action and "response_error" in self.action:
                if  self.action["cache_response"]:
                    cache = True
                else:
                    cache = False
                self.assistant.stop_conversation()
                self.play_response(event, cache=cache, error=True)
            elif self.action:
                self._feedback()
            self.clean()
            traceback.print_exc()
        print(self.args)
    def exit(self):
        self.playshell.close()
    def at_exit(self):
        atexit.register(self)
