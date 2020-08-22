
import sys
sys.path.insert(0, 'config')
import importlib
from importlib import machinery 
loader = importlib.machinery.SourceFileLoader('config', 'config/conf.py')
config = loader.load_module('config')
from plexapi.server import PlexServer
from plexapi.myplex import MyPlexAccount
from plexapi.audio import Artist, Album


class Plex_Server:
    def __init__(self):
        self.plex = None
        self.baseurl = f"http://{config.server_addr}:{config.server_port}"
        print(self.baseurl)
    def get_connection(self):
        # account = MyPlexAccount(config.email, config.password)
        # print(account.authenticationToken)
        # device = account.device(config.server)
        # print(device.publicAddress, device.token, device.key )
        # self.plex = account.resource(config.server).connect() # returns a PlexServer instance
        self.plex = PlexServer(self.baseurl, config.token)

    def list_movies(self, library_name):
        if self.plex == None:
            self.get_connection()
        movies = self.plex.library.section(library_name)
        for video in movies.search(unwatched=True):
            print(video.title)
        recently_added = movies.recently_added()
        for item in recently_added:
            print("[%s] %s" % (item.type, item.title))

    def agincourt(self):
        if self.plex == None:
            self.get_connection()
        title = "Agincourt"
        author = "Bernard Cornwell"
        agin_album = "Agincourt (Unabridged)"
        year = 2009
        genre = "Audiobook"
        duration = ( (16 * 60 * 60 ) + (13 * 60 ) + 45   ) * 1000
        audiobooks = self.plex.library.section("Audiobooks")
        print(audiobooks.albums())
        book = None
        for bookCand in audiobooks.searchTracks(title=title):
            book = bookCand
        print(book.__dict__)
        print(book.artist().__dict__)
        book.refresh()

        # artist = Artist()
        # album = Album()
        # album.genres = [genre]
        # print(album)


        
        



if __name__ == "__main__":
    server = Plex_Server()
    # server.agincourt()
    server.list_movies("Christmas")
    