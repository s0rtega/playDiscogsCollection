__version_info__ = (0,0,1)
__version__ = '0.0.1'

#requires pip install rauth
import urllib2 
import json
import time
import re
import webbrowser

from extractCatalogueFromJSON import CatalogueOperations
from spotify                  import SpotifyClient
from rauth                    import OAuth1Service
from random                   import choice

class DiscogsClient:
	
	def __init__(self):
		self.discogs = OAuth1Service(
				consumer_key='MZQKzvMRSllgLxwhfMsv',
				consumer_secret='xOVXcIEKdEnnTziVTWtxKOtUgpTjuQav',
				name='discogs',
				access_token_url='http://api.discogs.com/oauth/access_token',
				authorize_url='http://www.discogs.com/oauth/authorize',
				request_token_url='http://api.discogs.com/oauth/request_token',
				base_url='http://api.discogs.com/')				
		self.session = self.oauthLogin()		
	
	def getCatalog(self):
		catalogList=[]
		r = self.session.get(self.discogs.base_url+"oauth/identity", params={'User-agent' : 'GettingCollections Python2.7'})

		if r.status_code == 200: #Estamos identificados 
			releases = self.session.get( r.json()['resource_url']+"/collection/folders/0/releases", params={'User-agent' : 'gettingCollections Python2.7', 'per_page' : '100'}).json()	
			
			#with open ('catalog.json', 'w') as outfile:
			#		json.dump(releases,outfile)
					
			catalogList.append(releases)
			
			for i in range(1,int(re.compile('.*\&page=(.*)').match(releases['pagination']['urls']['last']).group(1))):			
				time.sleep(1)		
				releases = self.session.get( r.json()['resource_url']+"/collection/folders/0/releases", params={'User-agent' : 'GettingCollections Python2.7', 'per_page' : '100', 'page' : i+1}).json()
				#with open ('catalog.json', 'a') as outfile:
				#	json.dump(releases,outfile)
				catalogList.append(releases)

			return catalogList	
	def oauthLogin(self):		
		session = None
		
		try:
			with open('oauth.sec'):
				credentialsFile = open('oauth.sec', 'r')
				session = credentialsFile.read().split(";")			
				access_token = session[0]
				access_token_secret = session[1]
				session = self.discogs.get_session((access_token, access_token_secret))	
				
				
		except IOError:
			request_token, request_token_secret = self.discogs.get_request_token()
			authorize_url                       = self.discogs.get_authorize_url(request_token) 
			print 'Visit this URL in your browser: ' + authorize_url
			
			pin = raw_input('Enter PIN from browser: ')
			session = discogs.get_auth_session(request_token, request_token_secret,method='GET', data={'oauth_verifier': pin})
			
			credentialsFile = open('oauth.sec', 'w')
			credentialsFile.write(session.access_token+";"+session.access_token_secret)
			credentialsFile.close()
			
			access_token = session.access_token
			access_token_secret = session.access_token_secret	
			
		return session

if __name__ == "__main__":
	
	discogsClient = DiscogsClient() 
	catalogs = discogsClient.getCatalog()

	link = 'spotify:trackset:PlaylistName:'
	spotifyOp = SpotifyClient()
	
	allSongs = []
	
	try:
		for catalog in catalogs:
			catalogOp = CatalogueOperations(None,catalog)
			
			for band in catalogOp.getBands():
				for album in catalogOp.getAlbumsByBand(band):
					album = spotifyOp.searchAlbum(album,band,'json')
					if album is not None:
						songList = spotifyOp.searchAlbumSongs(album['href'])
						for song in songList:
							allSongs.append(song)
	except:
		print "Max. requests exceeded"
		
	for i in range(1, 100):
			song = choice(allSongs)
			allSongs.remove(song)
			link+=song+","
		
	webbrowser.open(link[:-1])