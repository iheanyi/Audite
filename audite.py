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
        image1=similarArtists[0].get_images(results=1)
        image2=similarArtists[1].get_images(results=1)
        image3=similarArtists[2].get_images(results=1)
        return simplejson.dumps(dict(simArtist1Name=similarArtists[0].name,simArtist1Image=image1[0]['url'],simArtist2Name=similarArtists[1].name,simArtist2Image=image2[0]['url'],simArtist3Name=similarArtists[2].name,simArtist3Image=image3[0]['url']))

config = {'/html':
                {'tools.staticdir.on': True,
                 'tools.staticdir.dir': MEDIA_DIR,
                }
        }

cherrypy.tree.mount(Audite(), '/', config=config)
cherrypy.engine.start()