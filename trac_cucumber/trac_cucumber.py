from trac.core import *
from trac.config import ExtensionOption
from trac.wiki.api import IWikiMacroProvider
from interfaces import *

from pkg_resources import resource_filename

class TracCucumberPlugin(Component):
    implements(IWikiMacroProvider)

    # definition of extension points
    database = ExtensionOption('cucumber', 'database', ICucumberDatabase,
        'CucumberDatabase', """Name of the component implementing the cucumber story database""")

    renderer = ExtensionOption('cucumber', 'story_renderer', ICucumberStoryRenderer,
        'CucumberStoryRenderer', """Name of the component implementing the cucumber story renderer""")

    observer = ExtensionOption('cucumber', 'observer', ICucumberObserver,
        'CommandCucumberObserver', """Name of the component listening to story events""")


    ### IWikiMacroProvider
    def get_macros(self):
        return ["CucumberStory"]

    def get_macro_description(self, name):
        return """
            Wrap a Cucumber story

            Usage:
            {{{
                #!CucumberStory
                #name: manage_login

                Feature: User login
                  In order to use the site
                  as an unauthenticated visitors
                  i want to be able to login

                  Scenario: Logging in
                    Given I am on the homepage
                    When I enter my login details
                    And press "Login"
                    Then I should see my name
            }}}

            name is required and must be unique.
        """

    def expand_macro(self, formatter, name, content):
        story_name, story = self.parse_story(content)
        return self.process_and_render_story(formatter, story_name, story)


    # actual logic
    def parse_story(self, content):
        lines = content.split("\n")

        name = filter(lambda l: l.startswith("#name:"), lines)[0].replace("#name:", "").strip()
        story = "\n".join(filter(lambda l: not l.startswith("#name:"), lines)).strip()

        return name, story

    def process_and_render_story(self, formatter, story_name, story):
        if self.database.is_new_story(story_name):
            self.database.save_story(story_name, story)
            self.observer.story_added(story_name, story)
            return self.renderer.render_new_story(formatter, story_name, story)

        elif self.database.is_changed_story(story_name, story):
            self.database.save_story(story_name, story)
            self.observer.story_edited(story_name, story)
            return self.renderer.render_changed_story(formatter, story_name, story)

        elif not self.database.has_output(story_name):
            return self.renderer.render_missing_output(formatter, story_name, story)

        else:
            output = self.database.get_story_output(story_name)
            return self.renderer.render_story_output(formatter, story_name, output)
