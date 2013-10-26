__version_info__ = (0,0,1)
__version__ = '0.0.1'

import json
import re

class CatalogueOperations:

	def __init__(self,path='catalog.json',jsonCatalog=None):
		self.path = path
		self.catalog = catalog = {}
		
		if jsonCatalog is None:
			self.loadCatalog()
		else:
			self.json_catalog = jsonCatalog
		
		self.exportCatalog()
		
	def loadCatalog(self):
		self.json_catalog = json.load(open(self.path, 'r'))
	
	def exportCatalog(self):
		for album in self.json_catalog['releases']:
			try:
				albumList = self.catalog[album['basic_information']['artists'][0]['name']]
				albumList.append(album['basic_information']['title'])
				artist = re.sub(r'\(.*\)', '',album['basic_information']['artists'][0]['name'])
				self.catalog[artist] = albumList
			except KeyError:
				albumList = []
				albumList.append(album['basic_information']['title'])
				artist = re.sub(r'\(.*\)', '',album['basic_information']['artists'][0]['name'])
				self.catalog[artist] = albumList

	def getAlbumsByBand(self,band):
		return self.catalog[band]

	def getBands(self):
		return self.catalog.keys()
		
	def getAlbums(self):
		for album in self.catalog.keys():
			print self.catalog[album]
			
if __name__ == "__main__":
	catalogOp = CatalogueOperations()

	# Avaible operations
	#--------------------
	catalogOp.getAlbums()
	
	for band in catalogOp.getBands():
		print band
		print catalogOp.getAlbumsByBand(band)
		
	print catalogOp.catalog
	
	

		
	