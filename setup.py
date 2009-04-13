from setuptools import setup

PACKAGE = 'TracCucumber'
VERSION = '0.1'

setup(name=PACKAGE,
      version=VERSION,
      packages=['trac_cucumber'],
      entry_points={'trac.plugins': '%s = trac_cucumber' % PACKAGE},
      package_data={'trac_cucumber': ['templates/*.html',
                                      'htdocs/*.css']}
)
