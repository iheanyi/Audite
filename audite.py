import cherrypy
import webbrowser
import os
import simplejson
import sys
from pyechonest import artist
from pyechonest import song
from pyechonest import config
import random
config.ECHO_NEST_API_KEY="C9ZG8F5C8NZKIIZFE"

MEDIA_DIR = os.path.join(os.path.abspath("."), u"html")

class Audite(object):
    @cherrypy.expose
    def index(self):
        return open(os.path.join(MEDIA_DIR, u'index.html'))

    @cherrypy.expose
    def submit(self,search_artist):
        cherrypy.response.headers['Content-Type'] = 'application/json'
        similarArtists=artist.similar(names=artist.Artist(search_artist).name,results=15)
        random.shuffle(similarArtists)      
        currentImage=artist.Artist(search_artist).get_images(results=5)
        #random.shuffle(currentImage)
        currentImageURL = currentImage[0]['url']
        tracks=song.search(artist=search_artist,song_min_hotttnesss=0.5,results=10)
        if(len(tracks)== 0):
            currentTrackName = "No Tracks Found!"
        else:
            currentTrackName=tracks[0].title

        currentArtist = artist.Artist(search_artist).name

        print currentTrackName, currentArtist
        image1=similarArtists[0].get_images(results=1)[0]
        image2=similarArtists[1].get_images(results=1)[0]
        image3=similarArtists[2].get_images(results=1)[0]
        print image1, image2, image3
        return simplejson.dumps(dict(currentTrack=currentTrackName, currentArtistName=currentArtist,currentArtistImage=currentImageURL,simArtist1Name=similarArtists[0].name,simArtist1Image=image1['url'],simArtist2Name=similarArtists[1].name,simArtist2Image=image2['url'],simArtist3Name=similarArtists[2].name,simArtist3Image=image3['url']))

config = {'/html':
                {'tools.staticdir.on': True,
                 'tools.staticdir.dir': MEDIA_DIR,
                }
        }

#print cherrypy.engine.signal_handler.signals


#cherrypy.tree.mount(Audite(), '/', config=config)
cherrypy.quickstart(Audite(), '/', config=config)
#cherrypy.engine.start()
# if hasattr(cherrypy.engine, 'signal_handler'):
#     cherrypy.engine.signal_handler.subscribe()
#     cherrypy.engine.signal_handler(2)

