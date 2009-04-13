from trac.core import *
from trac.util import escape, Markup
from trac.wiki.macros import WikiMacroBase

class CucumberStoryMacro(WikiMacroBase):
	"""
		This is the documentation
	"""

	def expand_macro(self, formatter, name, args):
		return "hallo hier"
