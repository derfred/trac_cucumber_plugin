from interfaces import *
from trac.config import PathOption
import os.path

class CucumberDatabase(Component):
    implements(ICucumberDatabase)

    story_directory = PathOption("cucumber", "story_directory")
    output_directory = PathOption("cucumber", "output_directory")

    def story_file_name(self, story_name):
        return os.path.join(self.story_directory, "%s.feature" % story_name)

    def output_file_name(self, story_name):
        return os.path.join(self.output_directory, "%s.output" % story_name)

    def save_story(self, story_name, story):
        story_file = open(self.story_file_name(story_name), "w")
        story_file.write(story)
        story_file.close()

    def is_new_story(self, story_name):
        return not os.path.exists(self.story_file_name(story_name))

    def is_changed_story(self, story_name, story):
        if self.is_new_story(story_name):
            return False

        story_file = open(self.story_file_name(story_name))
        written_story = story_file.read()
        story_file.close()

        return written_story != story

    def get_story_output(self, story_name):
        return None

    def has_output(self, story_name):
        return False
