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
		try:	
			if format == 'json':
				print "Buscando: "+self.strip_accents(album)+" Artist: "+artist.split(",")[0]	
				album = self.strip_accents(album).split("(")[0].split("-")[0].replace("&", "and").replace(" ", "%20")
				# TODO: Find a proper way to different album names
				if album == "Love%20Poems%20For%20Dying%20Children%20Act%20I%20":
					album = "Love%20Poems%20For%20Dying%20Children%20Act%201%20"	
				response = json.load(urllib2.urlopen(('http://ws.spotify.com/search/1/album.json?q='+album)))	
								
				for album in response['albums']:
					artist = self.strip_accents(artist.split(",")[0].replace("&","and"))
					albumArtist  = re.escape(album['artists'][0]['name'].split("-")[0].replace("&","and"))
					if re.findall(artist, albumArtist, re.IGNORECASE):
						print "Encontrado: "+album['name']
						return album
					elif re.findall(albumArtist, artist, re.IGNORECASE):
						print "Encontrado: "+album['name']
						return album
		except UnicodeEncodeError:
			print "Cant encode the title of the album"
			
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
	
	
		