from mycroft import MycroftSkill, intent_file_handler
import json
import requests

class HotCompagny(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('compagny.hot.intent')
    def handle_compagny_hot(self, message):
        self.speak_dialog('compagny.hot')

        url = "http://worldtimeapi.org/api/timezone/America/Toronto"
        headers = {'content-type': 'application/json'}
        r = requests.get(url, headers=headers)
        details = json.loads(r.text)
        self.speak_dialog(details)
        print(details)

def create_skill():
    return HotCompagny()

