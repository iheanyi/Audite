"""
Taylor Seale & Iheanyi Ekechukwu
"""

import cherrypy
import os
from mako.template import Template
from mako.lookup import TemplateLookup
lookup = TemplateLookup(directories=['html'])

class HomePage(object):
	@cherrypy.expose
	def index(self):
		tmpl = lookup.get_template("index.html")
		return tmpl.render()

conf = os.path.join(os.path.dirname(__file__), 'audite.config') 
cherrypy.quickstart(HomePage(),config=conf)