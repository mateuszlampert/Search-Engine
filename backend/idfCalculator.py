import os
import numpy as np
from tqdm import tqdm
import pickle

class IDFCalculator:
    def __init__(self, bag_of_words_by_document, dictionary, path_to_cached_idf_dictionary = './backend/cache/idf_by_token_dictionary.pickle'):
        self.no_documents = len(bag_of_words_by_document)
        self.bag_of_words_by_document = bag_of_words_by_document
        self.dictionary = dictionary
        self.idf_by_token_dictionary = dict()
        self.path_to_cached_idf_dictionary = path_to_cached_idf_dictionary

        if os.path.getsize(self.path_to_cached_idf_dictionary) == 0:
            print("Couldn't find cached IDF dictionary at {path_to_cached_idf_dictionary}. Creating new one from scratch...:(".format(path_to_cached_idf_dictionary = self.path_to_cached_idf_dictionary))
            self.create_idf_dictionary()
        else:
            print("Found and loaded cached IDF dictionary from {path_to_cached_idf_dictionary} . If you want to recreate it, use create_idf_dictiory() method.".format(path_to_cached_idf_dictionary = self.path_to_cached_idf_dictionary))
            with open(self.path_to_cached_idf_dictionary, 'rb') as file:
                self.idf_by_token_dictionary = pickle.load(file)

        
    def create_idf_dictionary(self):
        print("Started creating idf dictionary...")

        for token in tqdm(self.dictionary):
            count = 0
            for document in self.bag_of_words_by_document:
                if token in self.bag_of_words_by_document[document]:
                    count += 1
        
            self.idf_by_token_dictionary[token] = np.log(self.no_documents / count)
        
        print("Finished creating idf dictionary...")

        with open(self.path_to_cached_idf_dictionary, 'wb') as file:
            pickle.dump(self.idf_by_token_dictionary, file)
            print("Saved IDF dictionary to cache at {path_to_cached_idf_dictionary}".format(path_to_cached_idf_dictionary = self.path_to_cached_idf_dictionary))
    
    def token_idf(self, token):
        return self.idf_by_token_dictionary[token]