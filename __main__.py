from __future__ import print_function

import argparse
import os.path
import json
import google.oauth2.credentials
from google.assistant.library import Assistant
from google.assistant.library.event import EventType
from google.assistant.library.file_helpers import existing_file
from custom_assistant import CustomAssistant
import settings

def process_event(event, assistant, custom_assistant):
    if event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        custom_assistant.before_do()  # do something before process the event
        custom_assistant._feedback()  # audio_feedback
        print()
    if event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED:
        custom_assistant.process(event)  # process the event with the custom_assistant
    print(event)

    if (event.type == EventType.ON_CONVERSATION_TURN_FINISHED and
            event.args and not event.args['with_follow_on_turn']):
        custom_assistant.after_do()  # do something after process the event
        print()


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--credentials', type=existing_file,
                        metavar='OAUTH2_CREDENTIALS_FILE',
                        default=os.path.join(
                            os.path.expanduser('~/.config'),
                            'google-oauthlib-tool',
                            'credentials.json'
                        ),
                        help='Path to store and read OAuth2 credentials')
    args = parser.parse_args()
    with open(args.credentials, 'r') as f:
        credentials = google.oauth2.credentials.Credentials(token=None,
                                                            **json.load(f))

    with Assistant(credentials) as assistant:
        custom_assistant = CustomAssistant(assistant)  # load the assistant
        for event in assistant.start():
            process_event(event, assistant, custom_assistant)  # process the event


if __name__ == '__main__':
    main()
