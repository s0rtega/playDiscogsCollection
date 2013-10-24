__version_info__ = (0,0,1)
__version__ = '0.0.1'

import urllib2 
import json
import webbrowser
import unicodedata
import re

class SpotifyClient:

	def __init__(self,api_uri='http://ws.spotify.com/search/1/album'):
		self._api_uri = api_uri
		
	def searchAlbum(self,album,artist,format='json'):
		print "Buscando: "+self.strip_accents(album)+" Artist: "+artist.split(",")[0]
		if format == 'json':
			album = self.strip_accents(album).split("-")[0].replace("&", "and").replace(" ", "%20")
			response = json.load(urllib2.urlopen(('http://ws.spotify.com/search/1/album.json?q='+album)))
			for album in response['albums']:
				artist = self.strip_accents(artist.split(",")[0].replace("&","and"))
				albumName  = re.escape(album['artists'][0]['name'].split("-")[0].replace("&","and"))
				print artist+albumName
				if re.search(artist, albumName, re.IGNORECASE):
					print "Encontrado: "+album['name']
					return album	
				elif re.search(albumName, artist, re.IGNORECASE):
					print "Encontrado: "+album['name']
					return album	
			
	def searchAlbumSongs(self,albumUri,format='json'):
		#print 'http://ws.spotify.com/lookup/1/.json?uri='+albumUri+'&extras=track'
		if format == 'json':
			songList = []
			response = json.load(urllib2.urlopen(('http://ws.spotify.com/lookup/1/.json?uri='+albumUri+'&extras=track')))
			for song in response['album']['tracks']:
				songList.append(song['href'].replace("spotify:track:",""))

		return songList
		
	def strip_accents(self,s):
		return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')
			
if __name__ == "__main__":
	spotifyOp = SpotifyClient()

	album = spotifyOp.searchAlbum('El acto','Paralisis Permanente','json')
	songList = spotifyOp.searchAlbumSongs(album['href'])
	
	totalSongs = []
	link = 'spotify:trackset:PlaylistName:'
	for song in songList:
		link+=song+","
	
	webbrowser.open(link[:-1])
	
	
		