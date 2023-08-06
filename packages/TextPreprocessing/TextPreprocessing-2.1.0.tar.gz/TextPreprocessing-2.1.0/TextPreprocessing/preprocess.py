import re
from TextPreprocessing.utility import process_text

class preprocess:
    
    def __init__(self):
        self.__version__ = "2.1.0"
        self.obj = process_text()
        self.start = 1

    def cleanup(self, text, end):
        text = self.obj.clear_generic_entity(text)
        text = str(text).lower().replace('\\', '').replace('_', ' ')
        text = self.obj.convert_abbreviations(text)
        text = self.obj.clear_email_id(text)
        text = self.obj.clear_web_url(text)
        text = self.obj.clear_html_tags(text)
        text = self.obj.clear_binary_char(text)
        text = self.obj.clear_accented_chars(text)
        text = self.obj.clear_special_chars(text)
        text = self.obj.clear_duplicate_chars(text)
        text = self.obj.clear_stop_words(text)
        text = self.obj.lemetize(text)
        text = self.obj.lemetize(text)
        text = self.obj.correct_spelling(text)
        
        print(f"{self.start}/{end}", end="\r")
        self.start+=1
        return text
    
    def reset_start(self):
        self.start = 1