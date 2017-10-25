actions = {
        "^open (?P<url>.*?) in browser$": {
          "action": "open_in_browser",
          "response_success": "I opened <url> in your browser",
          "response_error": "I couldn't open <url> in the browser"
        },
        "^play (?P<query>.*?)$": {
          "action": "play_music",
          "response_error": "I couldn't play <query>"
        },
        "^play$": {
          "action": "play_music",
          "response_error": "I couldn't play music",
          "cache_response": True
        },
        "^next song$": {
          "action": "next_song"
        },
        "^previous song$": {
          "action": "previous_song"
        },
        "^stop music": {
          "action": "stop_music"
        },
        "^open (?P<command>.+?)$": {
          "action": "run_command",
          "response_success": "Working on it",
          "response_error": "Sorry. I couldn't do it"
        },
        "^close (?P<command>.*?)$": {
          "additional_args": [["close", True]],
          "action": "run_command",
          "response_success": "I closed <command>",
          "response_error": "I couldn't close <command>"
        },
        "^search for (?P<query>.*?)$": {
          "action": "search_for",
          "response_success": "Showing search results for <query> in browser",
          "response_error": "I couldn't search for <query>"
        }
}
