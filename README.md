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

**Configuration:**

The config.json file is very intuitive.

	* "browser" is how you call your favorite browser from the console.

	* "search_query" is the query used by your favorite search engine to search in the web.

	* "audio_feedback" is the address of the mp3 file that will be reproduced after each successfull action.

**Dependencies:**

	* Python 3.4

	* Google Assistant Library for Python

	* PyGame

	* Pexpect

	* mps-youtube

	* mpv Player

**Known bugs:**

	* Music from youtube will keep playing after exit google assistant with CTRL-Z, please use CTRL-C instead.
	If by mistake you didn't do this just use:

		killall mpsyt

**Why Summer assistant:**

The idea comes from the TV show Rick and Morty, where Morty is the assistant of Rick in his adventures... But google assistant has a femenine voice by default, so Summer, Morty's sister, would be more appropiate. You can be Rick, build great things.
