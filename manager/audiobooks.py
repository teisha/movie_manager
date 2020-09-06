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
        return self.bookList

    def process_book(self, book: dict):
        # book = next((item for item in self.bookList if item["title"] == book_name), dict())
        print("PROCESSING: ")
        # print(book)
        # print(book["genre"])
        print(book["author"])
        print(book["title"])
        # print(book["narrated_by"])
        # print(book["filename"])
        filename = get_orig_filename(book)
        if not os.path(filename).exists:
            print('Source file does not exist!')
            raise Exception('File Not Found')

        print("AUDIO INFO FOR : ", filename)
        audio = MP3(filename)

        print(audio.info.__dict__)
        print(audio.info.bitrate)
        # audio_id3 = ID3(filename, translate=False)
        # print(audio_id3.keys())
        print("ID3 TAG INFO: ")
        # print(EasyID3.valid_keys.keys())
        audio_id3 = EasyID3(filename)
        author = get_author(book)
        # release_date: datetime = None
        # try:
        #     datetime.datetime.strptime(book["release_date"], '%d-%b-%Y')
        # except:
        #     try:
        #         datetime.datetime.strptime(book["release_date"], '%Y-%b-%d')
        #     except:
        #         pass
        try:
            audio_id3["genre"] = [u"Audiobook", book["genre"] ]
        except:            
            audio_id3["genre"] = [u"Audiobook"]
        audio_id3["performer"] = book["narrated_by"]
        audio_id3["author"] = author
        if 'The Great Courses' in book['author']:
            audio_id3['artist'] = author
            audio_id3['albumartist'] = author
        # audio_id3["date"] = str(release_date.year)
        try:
            audio_id3['copyright'] = book["copyright"]
        except:
            pass
        try:
            audio_id3['language'] = book["language"]
        except:
            pass
        audio_id3['asin'] = book["asin"]
        audio.pprint()
        # audio_id3['length'] = math.floor(audio.info.length )
        audio_id3.save()
        # for keyname in EasyID3.valid_keys.keys():
        #     try:
        #         print (keyname , ":   ", audio_id3[keyname]   )
        #     except:
        #         pass
        self.move_file_to_desination(book)
                   
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
        # print("FILE TAGS:")
        # for frame in mutagen.File(filename).tags.getall("TXXX"):
        #     print("{} : {}".format(frame.desc , frame.text if frame.desc != 'json64' else "json stuff" ) )
        # print('TAGS:')
        # tag_file = mutagen.File(filename)
        # tags = tag_file.tags
        # # print(tags.keys())
        # # for tag in tags.keys():
        # #     if tag.startswith('T'):
        # #         try:
        # #             print(tag, ":   ", tag_file.tags[tag] )
        # #         except:
        # #             pass
        # print("OS FILE PROPERTIES: ")
        # os_file = os.stat(filename)
        # print(os_file)

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
        # keywords = ps.GetValue(pk).GetValue()
        # print(keywords)
        for keyname in keysToGet:
            print("{}: ".format(keyname), ps.GetValue(propsys.PSGetPropertyKeyFromName(keyname)).GetValue())
        
    def move_file_to_desination(self, book):
        # book["filename"]), author, book["filename"] = filename: str, author: str, title: str
        orig = get_orig_filename(book)
        print('Moving file ', orig)
        if not os.path(orig).exists:
            print('Source file does not exist!')
            raise Exception('File Not Found')
        dest_path = get_projected_destination_path(book)
        # "{}{}/{}/".format(config.dest_path,author, book_title  , filename )
        dest_file = "{}{}.mp3".format(dest_path, book['filename'] )
        print('Copy file to ', dest_file)
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        shutil.copy(orig, dest_file)

def get_orig_filename(book: dict):
    return "{}{}.mp3".format(config.origin_path,book["filename"])

def get_author(book: dict):
    return book["author"].replace(', The Great Courses','') 

def get_projected_destination_path(book):
    filename = book["filename"]
    book_title = book["filename"].replace(':','')
    author = get_author(book)
    dest_path = "{}{}/{}/".format(config.dest_path,author, book_title  , filename )
    return dest_path

if __name__ == "__main__":
    audioManager = AudioBookManager()
    all_books = audioManager.load_books()
    for book_title in [book['title'] for book in all_books]:
        print('*****************',book_title,'**************************')
        audioManager.process_book(book_title)
    # audioManager.process_book('Altered Carbon')










