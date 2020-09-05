import sys
sys.path.insert(0, 'manager')

import importlib
from importlib import machinery 
from _datetime import datetime
loader = importlib.machinery.SourceFileLoader('manager', 'manager/audiobooks.py')
manager = loader.load_module('manager')
from manager import get_projected_destination_path
import os

class Processor:
    def __init__(self):
        self.todaysdate = datetime.now()

    def get_new_books(self):
        audio_runner = manager.AudioBookManager()
        all_books = audio_runner.load_books()
        books_copied = []

        for book in all_books:
            print('*****************',book['title'],'**************************')
            projected_destination = get_projected_destination_path(book)
            filename = "{}{}.mp3".format(projected_destination, book['filename'] )
            print("Looking for: ", filename)
            if not os.path.isfile(filename):
                books_copied.append(filename)
                audio_runner.process_book(book)
            else:
                print("BOOK EXISTS: ", filename)  
        print(' ---------------------------------------------------------- ')
        print(" Processed %d books " % len(all_books) )   
        print(" There were {} books copied into the Plex folder: ".format(len(books_copied)))                 
        for file_destination in books_copied:
            print(file_destination)





if __name__ == "__main__":
    processor = Processor()
    processor.get_new_books()