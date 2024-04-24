import os
from collections import Counter
from bagOfWordsCreator import BagOfWordsCreator
from tqdm import tqdm
import pickle

class DictionaryCreator:
    def __init__(self, articles_dir = "./backend/articles", min_occurrences = 8, path_to_cached_dictionary = './backend/cache/dictionary.pickle', path_to_cached_bag_of_words_by_document = './backend/cache/bag_of_words_by_document.pickle'):
        self.articles_dir = articles_dir
        self.file_path_template = "{articles_dir}/{file}"
        self.file_dictionary_creator = BagOfWordsCreator()
        self.dictionary = Counter()
        self.bag_of_words_by_document = dict()
        self.min_occurrences = min_occurrences
        self.path_to_cached_dictionary = path_to_cached_dictionary
        self.path_to_cached_bag_of_words_by_document = path_to_cached_bag_of_words_by_document

        if os.path.getsize(self.path_to_cached_dictionary) == 0:
            print("Couldn't find cached dictionary at {path_to_cached_dictionary}. Creating new one from scratch...:(".format(path_to_cached_dictionary = self.path_to_cached_dictionary))
            self.create_dictionary()
        elif os.path.getsize(self.path_to_cached_bag_of_words_by_document) == 0:
            print("Couldn't find cached bag of words by document at {path_to_cached_bag_of_words_by_document}. Creating new one from scratch...:(".format(path_to_cached_bag_of_words_by_document = self.path_to_cached_bag_of_words_by_document))
            self.create_dictionary()
        else:
            print("Found and loaded cached dictionary from {path} . If you want to recreate it, use create_dictiory() method.".format(path = self.path_to_cached_dictionary))
            with open(self.path_to_cached_dictionary, 'rb') as file:
                self.dictionary = pickle.load(file)
            with open(self.path_to_cached_bag_of_words_by_document, 'rb') as file:
                self.bag_of_words_by_document = pickle.load(file)

    
    def create_dictionary(self):
        print("Started creating words dictionary...")
        for file in tqdm(os.scandir(self.articles_dir)):
            try:
                file_path = self.file_path_template.format(articles_dir=self.articles_dir, file=file.name)
                bag_of_words = self.file_dictionary_creator.create_bag_of_words_from_file(file_path)
                
                self.bag_of_words_by_document[file.name] = bag_of_words
                self.dictionary += bag_of_words
            except:
                pass

        print("Finished creating words dictionary...")
        
        self.filter_dictionary()

        with open(self.path_to_cached_dictionary, 'wb') as file:
            pickle.dump(self.dictionary, file)
            print("Saved directory to cache at {path_to_cached_dictionary}".format(path_to_cached_dictionary = self.path_to_cached_dictionary))

        with open(self.path_to_cached_bag_of_words_by_document, 'wb') as file:
            pickle.dump(self.bag_of_words_by_document, file)
            print("Saved bag of words by document to cache at {path_to_cached_bag_of_words_by_document}".format(path_to_cached_bag_of_words_by_document = self.path_to_cached_bag_of_words_by_document))

    def filter_dictionary(self):
        print("Started removing tokens occurring less than {min_occurrences} times...".format(min_occurrences=self.min_occurrences))
        
        items = len(self.dictionary)
        self.dictionary = {token: count for token, count in self.dictionary.items() if count >= self.min_occurrences}
        
        self.bag_of_words_by_document = {document: {token: count for token, count in counter.items() if token in self.dictionary} for document, counter in self.bag_of_words_by_document.items()}
        
        print("Finished filtering dictionary. Removed {removed} of {items} items".format(removed=items - len(self.dictionary), items=items))

d = DictionaryCreator()
print(len(d.dictionary.keys()))