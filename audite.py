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
        orig_artist = artist.Artist(search_artist)
        simArtists=[]
      	for i,similar_artist in enumerate(orig_artist.similar): 
       		simArtists.append(similar_artist.name)
       		if i==2:
       			break
        return simplejson.dumps(dict(simArtist1=simArtists[0],simArtist2=simArtists[1],simArtist3=simArtists[2]))

config = {'/html':
                {'tools.staticdir.on': True,
                 'tools.staticdir.dir': MEDIA_DIR,
                }
        }

cherrypy.tree.mount(Audite(), '/', config=config)
cherrypy.engine.start()