from adapt.intent import IntentBuilder
from mycroft.skills import intent_handler
from ovos_workshop.skills import OVOSSkill
from mycroft.skills.intent_services.adapt_service import AdaptIntent


class ReplaceSkillNameSkill(OVOSSkill):
    def initialize(self):
        """ Perform any final setup needed for the skill here.
        This function is invoked after the skill is fully constructed and
        registered with the system. Intents will be registered and Skill
        settings will be available."""
        my_setting = self.settings.get('my_setting')

    @intent_handler('HowAreYou.intent')
    def handle_how_are_you_intent(self, message):
        """ This is a Padatious intent handler.
        It is triggered using a list of sample phrases."""
        self.speak_dialog("how.are.you")

    @intent_handler(IntentBuilder('HelloWorldIntent')
                    .require('HelloKeyword').optionally("WorldKeyword"))
    def handle_hello_world_intent(self, message):
        """ Skills can log useful information. These will appear in the CLI and
        the skills.log file."""
        self.log.info("There are five types of log messages: "
                      "info, debug, warning, error, and exception.")
        self.speak_dialog("hello.world")

    @intent_handler(AdaptIntent('YesNoIntent').
                    one_of('YesKeyword', 'NoKeyword').
                    optionally("WorldKeyword"))
    def handle_yesno_world_intent(self, message):
        if message.data.get("YesKeyword"):
            self.speak("yes")
        else:
            self.speak("no")
        if message.data.get("WorldKeyword"):
            self.speak("world!")

    def stop(self):
        pass


def create_skill():
    return ReplaceSkillNameSkill()
