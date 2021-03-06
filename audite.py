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
import requests
import base64
import struct
import urllib

config.ECHO_NEST_API_KEY="C9ZG8F5C8NZKIIZFE"

HTML_DIR = os.path.join(os.path.abspath("."), u"html")
STATIC_DIR = os.path.join(os.path.abspath("."), u"static")
yt_service = gdata.youtube.service.YouTubeService()
similar=[]

class Audite(object):
    @cherrypy.expose
    def index(self):
        return open(os.path.join(HTML_DIR, u'index.html'))

    @cherrypy.expose
    def search(self,search_artist,user,new_search):
        cherrypy.response.headers['Content-Type'] = 'application/json'
        # This doesn't quite work yet, commented out for purpose of demonstration
        #if user=='1':
        #    if similar.__len__>1:
        #        if new_search=='1':
        #            del similar[0:len(similar)]
        #        if similar.__len__==5:
        #            print "Length is 5"
        #            del similar[1]
        #        if search_artist not in [art.name for art in similar]:
        #            similar.append(artist.Artist(search_artist))
        #    else:
        #        similar.append(artist.Artist(search_artist))
        #print [art.name for art in similar]
        similarArtists=artist.similar(names=artist.Artist(search_artist),results=50)
        random.shuffle(similarArtists)      
        currentImage=artist.Artist(search_artist).get_images(results=50)
        random.shuffle(currentImage)
        currentImageURL = currentImage[0]['url']
        tracks=song.search(artist=search_artist,song_min_hotttnesss=0.5,results=50)
        self.currentName = search_artist
        random.shuffle(tracks)
     

        currentArtist = artist.Artist(search_artist).name
        #print currentTrackName, currentArtist
        image1=similarArtists[0].get_images(results=50)
        random.shuffle(image1)
        image2=similarArtists[1].get_images(results=50)
        random.shuffle(image2)
        image3=similarArtists[2].get_images(results=50)
        random.shuffle(image3)
        #print image1, image2, image3

        if(len(tracks)== 0):

            tracks = song.search(artist=search_artist, results=10)

            if(len(tracks) == 0):
                currentTrackName = "No Track Found!"

            else:
                currentTrackName = tracks[0].title
        else:
            currentTrackName=tracks[0].title

        for t in tracks:
            streamLink = self.play_song(t.title, currentArtist)
            currentTrackName = t.title

            if(streamLink is None or streamLink is ""):
                continue
            else:
                print "Stream link getting returned is: " + streamLink
                if streamLink.__len__==0:
                    status="error"
                else:
                    status="success"
                return simplejson.dumps(dict(currentTrack=currentTrackName,currentArtistName=currentArtist,currentArtistImage=currentImageURL,simArtist1Name=similarArtists[0].name,simArtist1Image=image1[0]['url'],simArtist2Name=similarArtists[1].name,simArtist2Image=image2[0]['url'],simArtist3Name=similarArtists[2].name,simArtist3Image=image3[0]['url'],streamURL=streamLink,status=status))
 
        streamLink = self.play_song(currentTrackName, currentArtist)


        # if(streamLink is None or streamLink is ""):
        #     print "No stream link found, so we are going to start over . .  ."
        #     self.submit(currentArtist)
        # else:
        #     print "Stream link getting returned is: " + streamLink
        #     return simplejson.dumps(dict(currentTrack=currentTrackName,currentArtistName=currentArtist,currentArtistImage=currentImageURL,simArtist1Name=similarArtists[0].name,simArtist1Image=image1[0]['url'],simArtist2Name=similarArtists[1].name,simArtist2Image=image2[0]['url'],simArtist3Name=similarArtists[2].name,simArtist3Image=image3[0]['url'],streamURL=streamLink))

    def play_song(self, track_name, artist_name):
        yt_service = gdata.youtube.service.YouTubeService()
        query = gdata.youtube.service.YouTubeVideoQuery()
        query.vq = track_name + " " +  artist_name
        print query.vq
        query.orderby = 'relevance'
        query.start_index = 1
        query.max_results = 10
        query.racy = 'exclude'
        feed = yt_service.YouTubeQuery(query)
        for entry in feed.entry:
            song = entry
            streamURL = song.media.player.url
            #print streamURL
            link = self.getYouTubeHTML(streamURL)
            #print "Link Checking"
            if(link is None):
                #print "LINK IS NONE, TRYING NEXT VIDEO"
                continue
            else:
                #print "Returning the link!"
                #print link
                return link


    def getYouTubeHTML(self, vidURL):
        r = requests.get(vidURL)
        html = r.text

        html = html.split("var_swf = ")[-1]
        html = html.split("document.getElementById(")[0]
        #self.decodeURL(html)
        link = self.getURLs(html)
        return link

    def getURLs(self, content):

        newString = urllib.unquote(content)
        newString = urllib.unquote(newString)
        newString = urllib.unquote(newString)

        newString = newString.replace("\\u0026", "&")

        links = newString.split('url_encoded_fmt_stream_map\":')[-1]
        #print links

        qualities = links.split("url=")
        qualities.pop(0)
        i = 0
        cleanURLs = []
        for each in qualities:
            #print each
            #if("video/mp4" in each):

                #print "Checking if video/mp4 junts in there."
                #print each
            each = each.split(";+codecs=")[0]
            #print str(i) + ":" + qualities[i]

            contentDecoded = ""
            sigPattern = re.compile(r'sig=[0-9A-Z]{40}\.[0-9A-Z]{40}')


            

            if(("video/mp4" in each and "sig=" in each)): # or ("sig=" in each and "video/3gpp" in each)):
                #print each
                sigMatcher = sigPattern.search(each)
                #print "Valid URL!"
                #print each
                if(sigMatcher):
                    #print sigMatcher.group()
                   # realSignature = re.match(r'signature=[0-9A-Z]{40}\.[0-9A-Z]{40}', each)      
                    #print realSignature       
                    lastTag = each.split("&itag=")[-1]
                    url = each.split("&itag=" + lastTag)[0]
                    if("sig=" in url):
                        #print "Signature already there."
                        contentDecoded = url
                    #else:
                        #print "Signature not there."
                        #print "Appending signature"
                        #contentDecoded = url + "&" + sigMatcher.group()
                    #contentDecoded = contentDecoded.replace("x-flv", "flv")
                    #contentDecoded = re.sub(r'sig=[0-9A-Z]{40}\.[0-9A-Z]{40}.*', sigMatcher.group(), contentDecoded)
                    contentDecoded = contentDecoded.replace("sig=", "signature=")
                    #print "FINAL URL"
                    #print contentDecoded
                    cleanURLs.append(contentDecoded)

        #print qualities

        #contentDecoded = cleanURLs[0]

        #contentDecoded = contentDecoded.replace("sig=", "signature=")
        #contentDecoded = contentDecoded.replace("x-flv", "flv")
        #print "PRINTING CLEAN URLS"

        for e in cleanURLs:
            #print mime + " " + e
            if("fallback_host" in e 
                and "itag=22" not in e
                and "itag=43" not in e
                and "itag=102" not in e 
                and "itag=46" not in e 
                and "itag=34" not in e 
                and "itag=35" not in e 
                and "itag=45" not in e):
                return e
            #else:
                #print "Failed some test that I had . . . "

        # if("signature=" in contentDecoded):
        #     print "From conditional"
        #     print contentDecoded
        #     return simplejson.dumps(dict(streamURL=contentDecoded))
        #     #print contentDecoded
        #     #return simplejson.dumps(dict(streamURL=contentDecoded))
        # else:

        #     print "Retrying this junts . . . "
        #     tracks=song.search(artist=self.currentName,results=50)
        #     random.shuffle(tracks)
        #     currentTrackName=tracks[0].title
        #     self.play_song(currentTrackName, self.currentName)
        #     return simplejson.dumps(dict(currentTrack=currentTrackName))

    def parseCodecs(self, content):
        matcher = re.compile(',')
        match = matcher.search(content)
        if(match):
            qualities = matcher.split(content)
            #qualities = content.split(',')
            #print qualities[0:5]
            self.buildLinks(qualities[0], 1)

    def buildLinks(self, block, i):
        urlMatcher = re.compile(r'http:\/\/.*')
        match = urlMatcher.search(block)
        #print "BUILDING LINKS"
        if(match):
            #print "MATCH FOUND"
            sigPattern = re.compile(r'signature=[0-9A-Z]{40}\.[0-9A-Z]{40}')
            sigMatcher = sigPattern.search(block)
            if(sigMatcher):
                #print "AND ANOTHER ONE"
                urlString = match.group()
                urlString = re.sub(r"&type=.*", "", urlString)
                urlString = re.sub(r'&signature=.*', "", urlString)
                urlString = re.sub(r'&quality=.*', "", urlString)
                urlString = re.sub(r'&fallback_host=.*', "", urlString)

                sig = sigMatcher.group()
                link = urlString + "&" + sig
                link = re.sub(r'&itag=[0-9][0-9]&signature', "&signature", link)

                newlink = bytearray(link)

                #print newlink

                memLink = memoryview(link)
                #dlLink = bytes.decode(str(ink))
                #print link
                #print memLink.tobytes()
                #print dlLink
                #print urlString

    def decodeURL(self, html):
        #print html
        startPattern = re.compile('"url_encoded_fmt_stream_map": "')
        endPattern = re.compile(r'\\\", \\\\"')


        match = startPattern.search(html)

        if(match):
            #result = match.group(0)

            start = startPattern.split(html)
            end = endPattern.split(start[1])
 

            #print type(end[0])
            contentDecoded = urllib.unquote(end[0])
            contentDecoded = contentDecoded.replace(", ", "-")
            contentDecoded = contentDecoded.replace("sig=", "signature=")
            contentDecoded = contentDecoded.replace("x-flv", "flv")
            contentDecoded = contentDecoded.replace("\\u0026", "&")

            #print contentDecoded
            self.parseCodecs(contentDecoded)
            #print result
        #print r.text

        #self.PrintVideoFeed(feed)


config = {'/html':
                {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': HTML_DIR,
                },
           '/static':
           		{
           		'tools.staticdir.on': True,
				'tools.staticdir.dir': STATIC_DIR,
           		},
            'global':
                {
                'server.socket_host':'0.0.0.0',
                },


        }

cherrypy.config.update({'server.socket_host': '0.0.0.0',})
cherrypy.config.update({'server.socket_port': int(os.environ.get('PORT', '5000')),})


cherrypy.quickstart(Audite(), '/', config=config)