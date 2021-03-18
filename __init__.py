from mycroft import MycroftSkill, intent_file_handler


class HotCompagny(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('compagny.hot.intent')
    def handle_compagny_hot(self, message):
        self.speak_dialog('compagny.hot')


def create_skill():
    return HotCompagny()

