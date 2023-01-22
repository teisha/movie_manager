import pytest
import os
from manager import audiobooks

# python -m pytest test/test_audiobook_copy.py
class TestClass:
    def test_reads_booklist(self):
        print("GET BOOKLIST")
        audioManager = audiobooks.AudioBookManager()
        all_books = audioManager.load_books()
        # for book_title in [book['title'] for book in all_books]:
        #     print(book_title)
        assert "12 Strong - The Declassified True Story of the Horse Soldiers" in [book['title'] for book in all_books] 
        twelve_strong = next((book for book in all_books if "12 Strong - The Declassified True Story of the Horse Soldiers" == book['title'] ), None)
        print("TWELVE STRONG BOOK:: ",twelve_strong)
        audioManager.process_book(twelve_strong)
        assert os.path.exists('/mnt/m/Audiobooks/Doug Stanton/12 Strong.m4b')
        assert not os.path.exists('/mnt/m/Audiobooks/Doug Stanton/12 Strong.mp3') 


    '''
    TWELVE STRONG BOOK::  {'rating_average': '4.522622792160658', 
    'copyright': '©2009 Doug Stanton (P)2011 Simon & Schuster', 
    'chapters': [{'start_offset_ms': 0, 'length_ms': 357308, 'title': 'Opening Credits', 'start_offset_sec': 0}, {'start_offset_ms': 357308, 'length_ms': 1635289, 'title': 'Prologue', 'start_offset_sec': 357}, {'start_offset_ms': 1992597, 'length_ms': 6395705, 'title': 'Part One', 'start_offset_sec': 1993}, {'start_offset_ms': 8388302, 'length_ms': 13244755, 'title': 'Part Two', 'start_offset_sec': 8388}, {'start_offset_ms': 21633057, 'length_ms': 19821528, 'title': 'Part Three', 'start_offset_sec': 21633}, {'start_offset_ms': 41454585, 'length_ms': 6904267, 'title': 'Part Four', 'start_offset_sec': 41455}, {'start_offset_ms': 48358852, 'length_ms': 8908522, 'title': 'Part Five', 'start_offset_sec': 48359}, {'start_offset_ms': 57267374, 'length_ms': 2750868, 'title': 'Epilogue', 'start_offset_sec': 57267}], 
    'abridged': 'false', 'description': '12 Strong is the dramatic account of a small band of Special Forces soldiers who secretly entered Afghanistan following 9/11 and rode to war on horses against the Taliban....', 'language': 'english', 'title': '12 Strong - The Declassified True Story of the Horse Soldiers', 
    'info_link': 'https://www.audible.com/pd/B004VFQGRQ', 'duration': '16:40:00', 'author_link': 'https://www.audible.com/author/Doug+Stanton/B001K8EYMG', 'seconds': 60000, 'narrated_by': 'Jack Garrett', 
    'product_id': 'BK_SANS_005491', 'genre': 'History:Middle East', 
    'summary': '<p>"A thrilling action ride of a book" (<i>The New York Times</i> Book Review) - from Jerry Bruckheimer in theaters everywhere January 19, 2018 - the <i>New York Times</i> best-selling, true-life account of a US Special Forces team deployed to dangerous, war-ridden Afghanistan in the weeks following 9/11. </p> <p>Previously published as <i>Horse Soldiers</i>, <i>12 Strong</i> is the dramatic account of a small band of Special Forces soldiers who secretly entered Afghanistan following 9/11 and rode to war on horses against the Taliban. Outnumbered 40 to one, they pursued the enemy army across the mountainous Afghanistan terrain and, after a series of intense battles, captured the city of Mazar-i-Sharif. The bone-weary American soldiers were welcomed as liberators as they rode into the city. Then the action took a wholly unexpected turn. </p> <p>During a surrender of 600 Taliban troops, the Horse Soldiers were ambushed by the would-be POWs. Dangerously overpowered, they fought for their lives in the city\'s immense fortress, Qala-i-Janghi, or the House of War. At risk were the military gains of the entire campaign: if the soldiers perished or were captured, the entire effort to outmaneuver the Taliban was likely doomed. </p> <p>"A riveting story of the brave and resourceful American warriors who rode into Afghanistan after 9/11 and waged war against Al Qaeda" (Tom Brokaw), Doug Stanton\'s account touches the mythic. The soldiers on horses combined ancient strategies of cavalry warfare with 21st-century aerial bombardment technology to perform a seemingly impossible feat. Moreover, their careful effort to win the hearts of local townspeople proved a valuable lesson for America\'s ongoing efforts in Afghanistan. With "spellbinding...action packed prose...The book reads more like a novel than a military history...the Horse Soldier\'s secret mission remains the US military\'s finest moment in what has since arguably been a muddled war" (<i>USA TODAY</i>). </p>', 
    'author': 'Doug Stanton', 'image_url': 'https://m.media-amazon.com/images/I/51-jBYJP-zL._SL500_.jpg', 
    'title_short': '12 Strong', 'rating_count': '4133', 'download_link': 'https://cds.audible.com/download?asin=B004VFQGRQ&cust_id=_rFhj-yBoFkKPmC4xAq5RGYqSmGHrRhqqW-2XfGZSeaGX70JBGpiibRrOrOZ&codec=LC_64_22050_stereo&source=audible_iPhone&type=AUDI', 
    'filename': '12 Strong', 'release_date': '2012-12-07', 'ayce': 'false', 'publisher': 'Simon & Schuster Audio', 
    'asin': 'B004VFQGRQ', 'region': 'US', 'purchase_date': '2018-12-26'}
    '''