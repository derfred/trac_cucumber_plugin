from trac.core import *

class ICucumberDatabase(Interface):
  def save_story(story_name, story):
    """Save the given story under the given story_name"""

  def get_story_output(story_name):
    """retrieve the output for given story, None if story has not yet executed"""

  def is_new_story(story_name):
    """determine whether this story has been seen before"""

  def is_changed_story(story_name, story):
    """determine wheter this story is the same as the output for that story."""

  def has_output(story_name):
    """determine whether any output for this story is available."""


class ICucumberStoryRenderer(Interface):
  def render_new_story(formatter, story_name, story):
    """display new story message"""

  def render_changed_story(formatter, story_name, story):
    """display a message stating that the story has been changed"""

  def render_missing_output(formatter, story_name, story):
    """display a message stating that the story has not yet been run"""

  def render_story_output(formatter, story_name, story):
    """turn the output of the given story into HTML"""


class ICucumberObserver(Interface):
  def story_added(story_name, story, tags):
    """called when a new story is added"""

  def story_edited(story_name, story, tags):
    """called when an existing story is edited"""
