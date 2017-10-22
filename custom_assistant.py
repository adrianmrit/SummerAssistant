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
        self.playing_music = False  # When music is paused is considered as playing
        self.music_paused = False
        self.delete_file = None
        self.FNULL = open(os.devnull, 'w')  # needed to avoid output from subprocess.Popen

        # says wellcome message when the assistant starts
        tts = gTTS(text=settings.wellcome_txt, lang='en')
        if os.path.isfile("responses/wellcome.mp3"):
            pass
        else:
            tts.save("responses/wellcome.mp3")
        with open("actions.json", "r") as f:
            self.actions = json.load(f)
        with open("dictionary.json", "r") as f:
            self.dictionary = json.load(f)
        subprocess.Popen(["mpv", "responses/wellcome.mp3"], stdout=self.FNULL, shell=False)

    """Reset some values
    """
    def clean(self):
        self.args = None
        print("args cleaned")
        self.action = None
        print("action cleaned")
        self.function = None
        print("function cleaned")

    """Play audio feedback when there is no other answer
    """
    def _feedback(self):
        subprocess.Popen(["mpv", settings.audio_feedback], stdout=self.FNULL, shell=False)

    """Run <command> in the shell
       If shell in self.args killall will be added to the beginning
    """
    def run_command(self):  # run params
        if "close" in self.args:
            if self.args["command"] == "google-chrome":
                self.args["command"] = "chrome"
            subprocess.Popen(["killall", self.args["command"]], stdout=self.FNULL, shell=False)
        else:
            subprocess.Popen([self.args["command"]], stdout=self.FNULL, shell=False)

    """Open <url> in browser
    """
    def open_in_browser(self):  # run params
        subprocess.Popen([settings.browser, self.args["url"]], stdout=self.FNULL, shell=False)

    """Search for <query>
       The url for the search motor is loaded from settings.search_query
       The browser where the search results will be shown is loaded from settings.browser
    """
    def search_for(self):
        query = settings.search_query.format(urllib.quote(self.args["query"]))
        subprocess.Popen([settings.browser, query], stdout=self.FNULL, shell=False)

    """Try action one by one and check if the pattern match the speech
       and then start to process
    """
    def analice_text(self, text):
        for action in self.actions.keys():
            regex = re.compile(action)
            m = regex.search(text)
            if m:  # if there was a match
                self.action = self.actions[action].copy()  # copy the action so the original dictionary is not modificated by accident
                self.args = m.groupdict()  # get all variables from the speech

                # check if a variable has a value in dictionary.json
                # if there is a match the value of the variable will be changed for the one in the dictionary
                for key in self.args.keys():
                    if key in self.dictionary:
                        for word in self.dictionary[key].keys():
                            if self.args[key] == word:
                                self.args[key] = self.dictionary[key][word]

                if "additional_args" in self.action:
                    for arg in self.action["additional_args"]:
                        self.args.update({arg:True})
                break

    """Search for something in mpsyt and play all the results
    """
    def play_music(self):
        if not "query" in self.args and self.music_paused:
            self.music_paused = False
        else:
            if self.playing_music:
                self.playshell.sendcontrol("c")
            self.playshell.sendline('/' + self.args["query"])
            self.playshell.sendline("all")
            self.playshell.send(" ")
        self.playing_music = True

    """Play next song
    """
    def next_song(self):
        self.playshell.send('>')
        self.playshell.send(' ')
        self.playing_music = True

    """Play previous song"""
    def previous_song(self):
        self.playshell.send('<')
        self.playshell.send(' ')
        self.playing_music = True

    """Pause music"""
    def stop_music(self):
        if self.playing_music:
            self.playing_music = False
            self.music_paused = True

    """Do something before process a new event"""
    def before_do(self):
        if self.delete_file:
            os.remove(self.delete_file)
            self.delete_file = None
        if self.playing_music and not self.music_paused:
            self.playshell.send(' ')

    """Do something after process the event"""
    def after_do(self):
        if self.playing_music and not self.music_paused:
            self.playshell.send(' ')

    """If there is a success or error response for the action the assistant will talk the corresponding one
    """
    def play_response(self, event, cache=False, error=False):
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
            subprocess.Popen(["mpv", file_name], stdout=self.FNULL, shell=False)
        else:
            tts.save(file_name)
            subprocess.Popen(["mpv", file_name], stdout=self.FNULL, shell=False)
            self.delete_file = file_name

    """The most useless function in the world"""
    def no_action(self):
        pass

    """Make everithing work.
       This will call analice_text, if there is an action that match the speech
       the default response from the assistant will be ignored, the action
       executed with the parameters and the sound feedback or success/error response played
    """
    def process(self, event):
        self.analice_text(event.args["text"].lower())
        try:
            self.__getattribute__(self.action["action"])() # this will call the function
            self.assistant.stop_conversation()
            if self.action and "response_success" in self.action:
                if "cache_response" in self.action and self.action["cache_response"]:
                    cache = True
                else:
                    cache = False
                self.play_response(event, cache=cache)
            else:
                self._feedback()
            self.clean()  # clean vars
            print("CUSTOM ACTION")
        except:
            if self.action and "response_error" in self.action:
                if "cache_response" in self.action and self.action["cache_response"]:
                    cache = True
                else:
                    cache = False
                self.assistant.stop_conversation()
                self.play_response(event, cache=cache, error=True)
            elif self.action:
                self._feedback()
            self.clean()
            traceback.print_exc()

    """What to do before exit"""
    def exit(self):
        self.playshell.close()

    """Register exit function"""
    def at_exit(self):
        atexit.register(self)
