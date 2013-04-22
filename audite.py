import cherrypy
import webbrowser
import os
import simplejson
import sys
import re
from pyechonest import artist
from pyechonest import song
from pyechonest import config
import random
import gdata.youtube
import gdata.youtube.service
from BeautifulSoup import BeautifulSoup
import requests

config.ECHO_NEST_API_KEY="C9ZG8F5C8NZKIIZFE"

MEDIA_DIR = os.path.join(os.path.abspath("."), u"html")

yt_service = gdata.youtube.service.YouTubeService()

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
        self.play_song(currentTrackName, currentArtist)
        return simplejson.dumps(dict(currentTrack=currentTrackName, currentArtistName=currentArtist,currentArtistImage=currentImageURL,simArtist1Name=similarArtists[0].name,simArtist1Image=image1['url'],simArtist2Name=similarArtists[1].name,simArtist2Image=image2['url'],simArtist3Name=similarArtists[2].name,simArtist3Image=image3['url']))

    def play_song(self, track_name, artist_name):
        yt_service = gdata.youtube.service.YouTubeService()
        query = gdata.youtube.service.YouTubeVideoQuery()
        query.vq = track_name + artist_name
        query.orderby = 'relevance'
        query.start_index = 1
        query.max_results = 10
        query.racy = 'exclude'
        feed = yt_service.YouTubeQuery(query)
        song = feed.entry[0]
        streamURL = song.media.player.url
        #print streamURL

        self.getYouTubeHTML(streamURL)

    def getYouTubeHTML(self, vidURL):
        r = requests.get(vidURL)
        html = r.text
        self.decodeURL(html)

    def parseCodecs(self, content):
        matcher = re.compile(",")
        match = matcher.search(content)
        if(match):
            qualities = matcher.split(content)
            print qualities[0]

    def buildLinks(self, block, i):
        urlMatcher = re.compile("http://.*")

    def decodeURL(self, html):
        #print html
        startPattern = re.compile('"url_encoded_fmt_stream_map": "')
        endPattern = re.compile('\", \"')


        match = startPattern.search(html)

        if(match):
            #result = match.group(0)

            start = startPattern.split(html)
            end = endPattern.split(start[1])
            print len(end)
            print len(start)
            print end[0]

            contentDecoded = end[0].encode('raw_unicode_escape').decode('utf-8')
            contentDecoded.replace(", ", "-")
            contentDecoded.replace("sig=", "signature=")
            contentDecoded.replace("x-flv", "flv")
            contentDecoded.replace("\\\\u0026", "&")
            print contentDecoded

            self.parseCodecs(contentDecoded)
            #print result
        #print r.text

        #self.PrintVideoFeed(feed)

    def PrintVideoFeed(self, feed):
      for entry in feed.entry:
        self.PrintEntryDetails(entry)

    def PrintEntryDetails(self, entry):
      print 'Video title: %s' % entry.media.title.text
      print 'Video published on: %s ' % entry.published.text
      print 'Video description: %s' % entry.media.description.text
      #print 'Video category: %s' % entry.media.category[[]0].text
      print 'Video tags: %s' % entry.media.keywords.text
      print 'Video watch page: %s' % entry.media.player.url
      print 'Video flash player URL: %s' % entry.GetSwfUrl()
      print 'Video duration: %s' % entry.media.duration.seconds

      # show alternate formats
      for alternate_format in entry.media.content:
        if 'isDefault' not in alternate_format.extension_attributes:
          print 'Alternate format: %s | url: %s ' % (alternate_format.type,
                                                     alternate_format.url)

      # show thumbnails
      for thumbnail in entry.media.thumbnail:
        print 'Thumbnail url: %s' % thumbnail.url


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

