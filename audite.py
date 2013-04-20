import cherrypy
import webbrowser
import os
import simplejson
import sys
from pyechonest import artist
from pyechonest import config
config.ECHO_NEST_API_KEY="C9ZG8F5C8NZKIIZFE"

MEDIA_DIR = os.path.join(os.path.abspath("."), u"html")

class Audite(object):
    @cherrypy.expose
    def index(self):
        return open(os.path.join(MEDIA_DIR, u'index.html'))

    @cherrypy.expose
    def submit(self,search_artist):
        cherrypy.response.headers['Content-Type'] = 'application/json'
        similarArtists=artist.similar(names=artist.Artist(search_artist).name,results=3)
        return simplejson.dumps(dict(simArtist1=similarArtists[0].name,simArtist2=similarArtists[1].name,simArtist3=similarArtists[2].name))

config = {'/html':
                {'tools.staticdir.on': True,
                 'tools.staticdir.dir': MEDIA_DIR,
                }
        }

cherrypy.tree.mount(Audite(), '/', config=config)
cherrypy.engine.start()