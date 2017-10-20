**Get started:**

First of all you have to follow this guide from google:
https://developers.google.com/assistant/sdk/develop/python/

Install mps-youtube directly from the repository:

	sudo pip3 install -U git+https://github.com/mps-youtube/mps-youtube.git

Install youtube_dl

	sudo pip3 install youtube_dl

Set mpv as the player for mps-youtube:

	mpsyt set player mpv, set playerargs ,exit


Once you have your google assistant installed in your computer download this code and run \_\_main__.py

**Settings:**

The settings.py file is very intuitive.

	* "wellcome_txt" is the wellcome message when the assistant starts.

	* "browser" is how you call your favorite browser from the console.

	* "search_query" is the query used by your favorite search engine to search in the web.

	* "audio_feedback" is the address of the mp3 file that will be reproduced after each successfull action.

**New commands:**

When a user says somethings the assistant will check if the speech match an existent pattern. You can create this patterns using regular expressions in the file actions.json. For example:

		"^open (?P<url>.*?) in browser$": {
			"action": "open_in_browser",
			"response_success": "I opened <url> in your browser",
			"response_error": "I couldn't open <url> in the browser",
			"cache_response": true
		}

The first part is the regular expression. If user says "open github.com in the browser" it will run a function called open_in_browser and pass a dictionary of values like this:

		{"url": "github.com"}

If the function don't return with any error the response_success will be the answer of the assistant, otherwise response_error will be the answer.

If "cache_response" is true a mp3 file with the answer for that action will be saved so it doesn't have to downloadit again. This might be deleted in a future because it can create many files if you use many different commands.

You can also pass more args to the function by using:
	"additional_args": ["close"],
This will add {"close": True} to the dictionary passed to the function.

Commands should be created in an order where they won't conflict with other commands. For example, if you have:

	 	"do (?P<something>.*?) (?P<here>.*?)"

and

		"do (?P<something>.*?) here)"

"do my homework here" will match the first pattern.

**Dictionary:**

If you have this in dictionary.json:

	{
	  "command":{
	    "chrome": "google-chrome"
	  }
	}

And this action:

	"^open (?P<command>.+?)$": {
		"action": "run_command",
		"response_success": "I opened <command>",
		"response_error": "I couldn't open <command>",
		"cache_response": true
	},

If user says: "open chrome" the dictionary passed to the function will look like this:

	{"command": "google-chrome"}

**Dependencies:**

	* Python 3.4

	* Google Assistant Library for Python

	* gTTS

	* Pexpect

	* mps-youtube

	* mpv Player

**Known bugs:**

Music from youtube will keep playing after exit google assistant with CTRL-Z, please use CTRL-C instead.
If by mistake you didn't do this just use:

		killall mpsyt

**Why Summer assistant:**

The idea comes from the TV show Rick and Morty, where Morty is the assistant of Rick in his adventures... But google assistant has a femenine voice by default, so Summer, Morty's sister, would be more appropiate. You can be Rick, build great things.
