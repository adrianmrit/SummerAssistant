import getpass
dictionary = {
  "command":{
    "chrome": "google-chrome",
    "home": ["xdg-open", "/home/{}/".format(getpass.getuser())],
    "downloads": ["xdg-open", "/home/{}/Downloads".format(getpass.getuser())],
  }
}
