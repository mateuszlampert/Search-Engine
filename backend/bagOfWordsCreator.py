from preprocessor import Preprocessor
from collections import Counter

class BagOfWordsCreator:
    def __init__(self):
        self.preprocessor = Preprocessor()

    def create_bag_of_words_from_file(self, path):
        file = open(path, 'r', encoding = 'utf-8')
        text = file.read()
        
        return self.create_bag_of_words_from_text(text)
    
    def create_bag_of_words_from_text(self, text):
        tokens = self.preprocessor.preprocess(text)

        return Counter(tokens)