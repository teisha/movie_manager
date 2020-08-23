import json
import os
import shutil
import math
import datetime
import mutagen
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2
from mutagen.easyid3 import EasyID3


import sys
sys.path.insert(0, 'config')
import importlib
from importlib import machinery 
loader = importlib.machinery.SourceFileLoader('config', 'config/conf.py')
config = loader.load_module('config')
from audio_file_conf import keysToGet 

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
        print("PROCESSING: ")
        # print(book)
        # print(book["genre"])
        print(book["author"])
        print(book["title"])
        # print(book["narrated_by"])
        # print(book["filename"])
        filename = "{}{}.mp3".format(config.origin_path,book["filename"])
        if not os.path.isfile(filename):
            print("File does not exist", filename)
            return

        print("AUDIO INFO: ")
        audio = MP3(filename)

        print(audio.info.__dict__)
        print(audio.info.bitrate)
        # audio_id3 = ID3(filename, translate=False)
        # print(audio_id3.keys())
        print("ID3 TAG INFO: ")
        # print(EasyID3.valid_keys.keys())
        audio_id3 = EasyID3(filename)
        release_date: datetime = datetime.datetime.strptime(book["release_date"], '%d-%b-%Y')
        audio_id3["genre"] = [u"Audiobook", book["genre"] ]
        audio_id3["performer"] = book["narrated_by"]
        audio_id3["author"] = book["author"]
        # audio_id3["date"] = str(release_date.year)
        audio_id3['copyright'] = book["copyright"]
        audio_id3['language'] = book["language"]
        audio_id3['asin'] = book["asin"]
        audio.pprint()
        # audio_id3['length'] = math.floor(audio.info.length )
        audio_id3.save()
        for keyname in EasyID3.valid_keys.keys():
            try:
                print (keyname , ":   ", audio_id3[keyname]   )
            except:
                pass
                   
        # print(audio_id3["genre"])
        # print(audio_id3["artist"])
        # print(audio_id3["albumartist"])
        # print(audio_id3["album"])
        # print(audio_id3["title"])
        # try:
        #     print(audio_id3["performer"])
        # except:
        #     print('Performer not found')
        # audio_id3["artist"] = book["author"]
        # audio_id3["albumartist"] = book["author"]
        # audio_id3["album"] = book["title"]
        # audio_id3["title"] = book["title"]

# artist
# albumartist
# album
# title
# performer    
        # audio_id3.save()
        print("FILE TAGS:")
        for frame in mutagen.File(filename).tags.getall("TXXX"):
            print("{} : {}".format(frame.desc , frame.text if frame.desc != 'json64' else "json stuff" ) )
        print('TAGS:')
        tag_file = mutagen.File(filename)
        tags = tag_file.tags
        print(tags.keys())
        for tag in tags.keys():
            if tag.startswith('T'):
                try:
                    print(tag, ":   ", tag_file.tags[tag] )
                except:
                    pass
        print("OS FILE PROPERTIES: ")
        os_file = os.stat(filename)
        print(os_file)

        self.move_file_to_desination("{}.mp3".format(book["filename"]), book["author"], book["title"])
# System.Audio.ChannelCount:  2
# System.Audio.Compression:  None
# System.Audio.EncodingBitrate:  55584
# System.Audio.Format:  {00000055-0000-0010-8000-00AA00389B71}
# System.Audio.IsVariableBitRate:  True
# System.Audio.PeakValue:  None
# System.Audio.SampleRate:  22050
# System.Audio.SampleSize:  16        
# System.Media.Duration:  584256522448        
# System.Media.EncodingSettings:  Lavf58.35.102
# System.Media.Year:  2009        
# System.Music.AlbumArtist:  Bernard Cornwell
# System.Music.AlbumTitle:  Agincourt (Unabridged)
# System.Music.Artist:  ['Bernard Cornwell'] 
# System.Music.Genre:  ['Audiobook']     
# System.Author:  ['Bernard Cornwell']
# System.ComputerName:  DESKTOP-KI6MHU3
# System.FileName:  Agincourt.mp3
# System.FileOwner:  DESKTOP-KI6MHU3\laima  

    def get_windows_sys_props(self, filename):
        print("WIN32COM.PROPSYS FILE PROPERTIES: ")
        pk = propsys.PSGetPropertyKeyFromName("System.Keywords")
        # get property store for a given shell item (here a file)
        #  MAKE SURE YOU USE THE RIGHT SLASHES HERE:
        ps = propsys.SHGetPropertyStoreFromParsingName(filename.replace('/','\\'))
#  build an array of string type PROPVARIANT
# newValue = propsys.PROPVARIANTType(["hello", "world"], pythoncom.VT_VECTOR | pythoncom.VT_BSTR)

# # write property
# ps.SetValue(pk, newValue)
# ps.Commit()
        # read & print existing (or not) property value, System.Keywords type is an array of string
        title = ps.GetValue(pscon.PKEY_Title).GetValue()
        print (title)
        print("System.Audio.Format", ps.GetValue(propsys.PSGetPropertyKeyFromName("System.Audio.Format")).GetValue())
        keywords = ps.GetValue(pk).GetValue()
        print(keywords)
        for keyname in keysToGet:
            print("{}: ".format(keyname), ps.GetValue(propsys.PSGetPropertyKeyFromName(keyname)).GetValue())
        

    def move_file_to_desination(self, filename: str, author: str, title: str):
        orig = config.origin_path + filename
        dest_path = "{}{}/{}/".format(config.dest_path,author, title  , filename )
        dest_file = "{}{}".format(dest_path  , filename )
        print('Copy file to ', dest_file)
        # Move a file from the directory d1 to d2
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        shutil.move(orig, dest_file)


if __name__ == "__main__":
    audioManager = AudioBookManager()
    audioManager.load_books()
    audioManager.process_book('Agincourt')
    # audioManager.process_book('Altered Carbon')










