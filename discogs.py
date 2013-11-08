__version_info__ = (0,0,1)
__version__ = '0.0.1'

import urllib2 
import json
import time
import re
import webbrowser
import os
import requests
import glob

from rauth	import OAuth1Service

class DiscogsClient:
	
	# Init. Preparing the info for oAuth
	def __init__(self):
		self._discogsOauth = OAuth1Service(
				consumer_key='XXXXXXXXXXXXXXXXX',
				consumer_secret='XXXXXXXXXXXXXXXX',
				name='discogs',
				access_token_url='http://api.discogs.com/oauth/access_token',
				authorize_url='http://www.discogs.com/oauth/authorize',
				request_token_url='http://api.discogs.com/oauth/request_token',
				base_url='http://api.discogs.com/')	

	# Get requested URL
	def fetchRequest(self,request,url,params):
		r = request.get(url,params=params)
		return r
	
	# Get User catalog
	def fetchCatalog(self,type,username=None,authRequest=None):
		catalogList = []
		
		# If private the auth is required
		if type == "private":
			sender = self._session
			username = authRequest['username']
			url = authRequest['resource_url']+"/collection/folders/0/releases"
		elif type == "public":
			sender = requests
			url = "http://api.discogs.com/users/"+username+"/collection/folders/0/releases"

		releases = self.fetchRequest(sender,url,{'User-agent' : 'gettingCollections Python2.7', 'per_page' : '100'}).json()
		
		# Prepare path to save the catalogs/info
		if not os.path.exists('./catalogs/'):
			os.makedirs('./catalogs/')
		with open ('./catalogs/catalog'+username+'.json', 'w') as outfile:
				json.dump(releases,outfile) # Save to file
	
		catalogList.append(releases)
		
		# If all the pages in the catalog requested
		try:
			for i in range(1,int(re.compile('.*\&page=(.*)').match(releases['pagination']['urls']['last']).group(1))):			
				time.sleep(1)
				releases = self.fetchRequest(sender,url,{'User-agent' : 'GettingCollections Python2.7', 'per_page' : '100', 'page' : i+1}).json()								
				with open ('catalogs/catalog'+username+str(i)+'.json', 'w') as outfile:
					json.dump(releases,outfile)
				catalogList.append(releases)							
		except KeyError: # No existe mas de una pagina
			pass
			
		return catalogList
		
	def getCatalog(self,username,force):
		exists = False
		# Checks if there is a catalog downloaded
		if (os.path.exists('./catalogs/catalog'+username+'.json') and force == False):
			catalogList = glob.glob('./catalogs/catalog'+username+'*.json')
			exists = True
			return catalogList,exists	
		
		# If not, connect to discogs		
		else:
			request = self.fetchRequest(requests,"http://api.discogs.com/users/"+username+"/collection/folders/0/releases", "{'User-agent' : 'gettingCollections Python2.7', 'per_page' : '1'}") # Test if the collection can be downloaded

			if request.status_code == 401: #User auth is required
				authRequest = self.getAuthLogin()
				if authRequest['username'] != username:
					print "This collection is private and you dont have access, search for another collection"
					exit()					
				else:
					print "Private collection. Fetching..."
					catalogList = self.fetchCatalog("private",None,authRequest)			
					return catalogList,exists
			elif request.status_code == 404: #Collection not found
					print "This resource is not avaible"
					exit()
			else: # No auth required
				print "Public collection. Fetching..."
				catalogList = self.fetchCatalog("public",username,None)			
				return catalogList,exists
				
	# Login method
	def getAuthLogin(self):
		self._session = self.oauthLogin() 
		r = self._session.get(self._discogsOauth.base_url+"oauth/identity", params={'User-agent' : 'GettingCollections Python2.7'}).json()	
		return r
		
	def oauthLogin(self):           
		session = None
		
		try:
			with open('./sec/oauth.sec'):
					credentialsFile = open('./sec/oauth.sec', 'r')
					session = credentialsFile.read().split(";")                     
					access_token = session[0]
					access_token_secret = session[1]
					session = self._discogsOauth.get_session((access_token, access_token_secret)) 
					
		except IOError:
				request_token, request_token_secret = self._discogsOauth.get_request_token()
				authorize_url                       = self._discogsOauth.get_authorize_url(request_token) 
				print 'Visit this URL in your browser: ' + authorize_url
				webbrowser.open(authorize_url)
				
				pin = raw_input('Enter PIN from browser: ')
				session = self._discogsOauth.get_auth_session(request_token, request_token_secret,method='GET', data={'oauth_verifier': pin})
				
				if not os.path.exists('./sec/'):
								os.makedirs('./sec/')                   
				credentialsFile = open('./sec/oauth.sec', 'w')
				credentialsFile.write(session.access_token+";"+session.access_token_secret)
				credentialsFile.close()
				
				access_token 		= session.access_token
				access_token_secret = session.access_token_secret       
				
		return session		
