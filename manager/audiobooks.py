import json
import os
import mutagen
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2


import sys
sys.path.insert(0, 'config')
import importlib
from importlib import machinery 
loader = importlib.machinery.SourceFileLoader('config', 'config/conf.py')
config = loader.load_module('config')

import pythoncom
from win32com.propsys import propsys, pscon
from win32com.shell import shellcon



class AudioBookManager:
    def __init__(self):
        print(' ============= started =================')

    def load_books(self):
        self.bookList=None
        with open(config.book_file_name, "rb") as handle:
        # with open('filename.pickle', 'rb') as handle:
            self.bookList = json.load(handle)
        # for book in self.bookList:
        #     print(book.get('title') )
        print("Files loaded", len(self.bookList)  )

    def process_book(self, book_name: str):
        book = next((item for item in self.bookList if item["title"] == book_name), dict())
        print("AMAZON METADATA: ")
        print(book)
        filename = "{}{}.mp3".format(config.origin_path,book["filename"])
        print("AUDIO INFO: ")
        audio = MP3(filename)
        print(audio.info.__dict__)
        print(audio.info.bitrate)
        audio_id3 = ID3(filename, translate=False)
        print("ID3 TAG INFO: ")
        print (audio_id3.keys())
        for frame in mutagen.File(filename).tags.getall("TXXX"):
            print(frame.__dict__)
            print("{}".format(frame.desc ) )
        print('TAGS:')
        tags=mutagen.File(filename).tags
        print(tags.keys())
        print("OS FILE PROPERTIES: ")
        os_file = os.stat(filename)
        print(os_file)

        print("WIN32COM.PROPSYS FILE PROPERTIES: ")
        pk = propsys.PSGetPropertyKeyFromName("System.Keywords")
        # get property store for a given shell item (here a file)
        print(pk)
        #  MAKE SURE YOU USE THE RIGHT SLASHES HERE:
        ps = propsys.SHGetPropertyStoreFromParsingName(filename.replace('/','\\'))
        # read & print existing (or not) property value, System.Keywords type is an array of string
        title = ps.GetValue(pscon.PKEY_Title).GetValue()
        print (title, pscon)
        keywords = ps.GetValue(pk).GetValue()
        print(keywords)



if __name__ == "__main__":
    audioManager = AudioBookManager()
    audioManager.load_books()
    audioManager.process_book('Agincourt')