__version_info__ = (0,0,1)
__version__ = '0.0.1'

import urllib2 
import json
import webbrowser
import unicodedata
import re
import os
import webbrowser

from extractCatalogueFromJSON import CatalogueOperations
from random                   import choice

class SpotifyClient:

	def __init__(self,api_uri='http://ws.spotify.com/search/1/album'):
		self._api_uri = api_uri
		
	# Search album (only json avaible)
	def searchAlbum(self,album,artist,format='json'):
		try:	
			if format == 'json':
				print "searching: "+self.strip_accents(album)+" Artist: "+artist.split(",")[0]	
				album = self.strip_accents(album).split("(")[0].split("-")[0].replace("&", "and").replace(" ", "%20")
				# TODO: Find a proper way to treat different album names. RegExprs?
				if album == "Love%20Poems%20For%20Dying%20Children%20Act%20I%20":
					album = "Love%20Poems%20For%20Dying%20Children%20Act%201%20"	
				response = json.load(urllib2.urlopen(('http://ws.spotify.com/search/1/album.json?q='+album)))	
							
				# Perform various check and operations to get the albums... (A better way is mandatory...)
				for album in response['albums']:
					artist = self.strip_accents(artist.split(",")[0].replace("&","and"))
					albumArtist  = re.escape(album['artists'][0]['name'].split("-")[0].replace("&","and"))
					if re.findall(artist, albumArtist, re.IGNORECASE):
						print "Found: "+album['name']
						return album
					elif re.findall(albumArtist, artist, re.IGNORECASE):
						print "Found: "+album['name']
						return album
		except UnicodeEncodeError:
			print "Cant encode the title of the album"
			
	# Get all the identifies from avaible album
	def searchAlbumSongs(self,albumUri,format='json'):
		#print 'http://ws.spotify.com/lookup/1/.json?uri='+albumUri+'&extras=track'
		if format == 'json':
			songList = []
			response = json.load(urllib2.urlopen(('http://ws.spotify.com/lookup/1/.json?uri='+albumUri+'&extras=track')))
			for song in response['album']['tracks']:
				songList.append(song['href'].replace("spotify:track:",""))

		return songList
		
	# Main method to get all the songs from the catalog, search first is downloaded catalog is avaible
	def getSongsFromCatalog(self,catalogs,force,exists,username):
		allSongs = []
		if not os.path.exists('./songs/'):		
			os.makedirs('./songs/')
		if (not os.path.exists('./songs/allSongs'+username+'.lst') or force==True):					
			for catalog in catalogs:
				catalogOp = None
				if not exists:
					catalogOp = CatalogueOperations(None,catalog)
				else:
					catalogOp = CatalogueOperations('./catalogs/'+catalog)

				for band in catalogOp.getBands():
					for album in catalogOp.getAlbumsByBand(band):
						album = self.searchAlbum(album,band,'json')
						if album is not None:
							songList = self.searchAlbumSongs(album['href'])
							for song in songList:
								allSongs.append(song)			
								
				with open ('./songs/allSongs'+username+'.lst', 'w') as outfile:
					for song in allSongs:
						print>>outfile, song
		else:
			with open('./songs/allSongs'+username+'.lst', 'r') as f:
				allSongs = f.read().splitlines()
		return allSongs
		
	# Prepare the URI to play random 100 songs from list 
	def getURIforSongs(self,allSongs):
		link = 'spotify:trackset:PlaylistName:'
		try:
			for i in range(1, 100):
				song = choice(allSongs)
				allSongs.remove(song)
				link+=song+","
		except IndexError:
			print "No avaible songs for this resource"
			exit()
		return link
	
	def playSpotifyURI(self,uri):
		webbrowser.open(uri[:-1])
		
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
		