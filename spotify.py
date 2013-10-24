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
			response = json.load(urllib2.urlopen(('http://ws.spotify.com/search/1/album.json?q='+self.strip_accents(album).replace(" ", "%20"))))
			for album in response['albums']:
				if re.search( self.strip_accents(artist.split(",")[0]), re.escape(album['artists'][0]['name'].replace("&","and")),re.IGNORECASE):
					print "Encontrado: "+album['name']
					return album	
				elif re.search(re.escape(album['artists'][0]['name'].replace("&","and")), self.strip_accents(artist.split(",")[0]),re.IGNORECASE):
					print "Encontrado: "+album['name']
					return album	
					
		elif format == 'xml': # No sirve de nada
			response = json.load(urllib2.urlopen((self._api_uri+'?q='+album).replace(" ", "%20")))	
			
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
	
	
		