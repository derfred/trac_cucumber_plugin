from interfaces import *
from data_model import *
from trac.config import PathOption
from xml.etree.ElementTree import ElementTree
import os.path, glob, os, stat

class CucumberDatabase(Component):
    implements(ICucumberDatabase)

    story_directory = PathOption("cucumber", "story_directory")
    output_directory = PathOption("cucumber", "output_directory")

    def story_file_name(self, story_name):
        return os.path.join(self.story_directory, "%s.feature" % story_name)

    def output_file_name(self, story_name):
        return os.path.join(self.output_directory, "%s.output" % story_name)


    ### ICucumberDatabase
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
        # find all potential output files and sort them by reverse modification time
        files = glob.glob(self.output_directory + "/*.output")
        files.sort(lambda a,b: cmp(os.stat(b)[stat.ST_MTIME], os.stat(a)[stat.ST_MTIME]))

        # now find the first file that contains output for the story_name
        tree = ElementTree()
        for f in files:
            tree.parse(f)
            for feature in tree.getiterator("feature"):
                if feature.attrib['name'] == (story_name + ".feature"):
                    return parse_feature_from_xml(feature)
        return None

    def has_output(self, story_name):
        return self.get_story_output(story_name) != None
