from interfaces import *
from trac.config import Option
import os

class CommandCucumberObserver(Component):
    implements(ICucumberObserver)

    story_added_callback = Option("cucumber", "story_added_callback")
    story_edited_callback = Option("cucumber", "story_edited_callback")

    def story_added(self, story_name, story):
        if self.story_added_callback:
            os.system("%s %s" % (self.story_added_callback, story_name))

    def story_edited(self, story_name, story):
        if self.story_edited_callback:
            os.system("%s %s" % (self.story_edited_callback, story_name))
