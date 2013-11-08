__version_info__ = (0,0,1)
__version__ = '0.0.1'

import argparse

from discogs	import DiscogsClient	
from spotify	import SpotifyClient

if __name__ == "__main__":
	
	# Parse arguments
	parser = argparse.ArgumentParser(description='Fetch a collection on discogs and play it on Spotify')
	parser.add_argument('-u','--user',  type=str, required=True,  help='User collection to play on Spotify')
	parser.add_argument('-f','--force', required=False, action='store_true', help='Force to update the collection')
	args = parser.parse_args()

	# Import discogs and spotify classes
	discogsClient = DiscogsClient() 
	spotifyOp = SpotifyClient()
	
	# Get catalogs
	catalogs,exists = discogsClient.getCatalog(args.user,args.force)

	# Get all songs from the request catalog
	allSongs = spotifyOp.getSongsFromCatalog(catalogs,args.force,exists,args.user)	
	uri = spotifyOp.getURIforSongs(allSongs)
	
	# Send link to spotify
	spotifyOp.playSpotifyURI(uri)