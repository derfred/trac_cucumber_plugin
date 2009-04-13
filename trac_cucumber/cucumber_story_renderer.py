from trac.util.html import Markup
from trac.wiki import Formatter
from trac.web.chrome import Chrome, ITemplateProvider, add_stylesheet
from interfaces import *

from pkg_resources import resource_filename

class CucumberStoryRenderer(Component):
    implements(ICucumberStoryRenderer, ITemplateProvider)

    ### ITemplateProvider methods
    def get_htdocs_dirs(self):
        return [('trac_cucumber', resource_filename(__name__, 'htdocs'))]

    def get_templates_dirs(self):
        return [resource_filename(__name__, 'templates')]


    ### ICucumberStoryRenderer methods
    def render_new_story(self, formatter, story_name, story):
        add_stylesheet(formatter.req, 'trac_cucumber/trac_cucumber.css')
        return Chrome(self.env).render_template(formatter.req, 'new_story.html', {'story_name': story_name, 'story': story})

    def render_changed_story(self, formatter, story_name, story):
        add_stylesheet(formatter.req, 'trac_cucumber/trac_cucumber.css')
        return Chrome(self.env).render_template(formatter.req, 'changed_story.html', {'story_name': story_name, 'story': story})

    def render_missing_output(self, formatter, story_name, story):
        add_stylesheet(formatter.req, 'trac_cucumber/trac_cucumber.css')
        return Chrome(self.env).render_template(formatter.req, 'missing_output.html', {'story_name': story_name, 'story': story})

    def render_story_output(self, formatter, story_name, output):
        add_stylesheet(formatter.req, 'trac_cucumber/trac_cucumber.css')
        return Chrome(self.env).render_template(formatter.req, 'story_output.html', {'story_name': story_name, 'output': output})
