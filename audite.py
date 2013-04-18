"""
Taylor Seale & Iheanyi Ekechukwu
"""

import cherrypy
from mako.template import Template
from mako.lookup import TemplateLookup
lookup = TemplateLookup(directories=['html'])

class HomePage(object):
	@cherrypy.expose
	def index(self):
		tmpl = lookup.get_template("index.html")
		return tmpl.render(salutation="Hello", target="World")

cherrypy.quickstart(HomePage(),'/','audite.config')