import sys
sys.path.insert(0, 'manager')

import importlib
from importlib import machinery 
from _datetime import datetime

loader = importlib.machinery.SourceFileLoader('manager', 'manager/audiobooks.py')
manager = loader.load_module('manager')
from manager import get_projected_destination_path, get_scrubbed_title

import os

class Processor:
    def __init__(self):
        self.todaysdate = datetime.now()

    def get_new_books(self):
        audio_runner = manager.AudioBookManager()
        all_books = audio_runner.load_books()
        books_copied = []
        books_errored = []

        for book in all_books:
            print('*****************',book['title'],'**************************')
            projected_destination = get_projected_destination_path(book)
            filename = "{}{}.m4b".format(projected_destination, book['filename'] )
            print("Looking for: ", filename)
            if not os.path.isfile(filename):
                try:
                    audio_runner.move_file_to_desination(book)
                    books_copied.append(filename)
                    print('File copied without errors::  ', filename)
                except Exception as e:
                    print("FAILED:: " + filename, e)
                    books_errored.append(filename)
            else:
                print("BOOK EXISTS - Nothing to do here ") 

        print(' ---------------------------------------------------------- ')
        print(" Processed %d books " % len(all_books) )   
        books_copied.sort()
        print(" There were {} books copied into the Plex folder: ".format(len(books_copied)))                 
        for file_destination in books_copied:
            print(file_destination)
        print(" ---------   ")
        print(" Errors occurred with the following files: ")
        for file_destination in books_errored:
            print(file_destination) 

    # used when files converted to new format
    def remove_mp3file(book: dict):
        projected_destination = get_projected_destination_path(book)
        oldfilename = "{}{}.mp3".format(projected_destination, get_scrubbed_title(book) ) 
        print ("SEARCHING FOR MP3 VERSION:: ", oldfilename)
        if os.path.isfile(oldfilename):
            print ("Found.  Deleting.")
            os.remove(oldfilename)
        else:
            print("MP3 file not removed", oldfilename)
            return oldfilename




if __name__ == "__main__":
    processor = Processor()
    processor.get_new_books()