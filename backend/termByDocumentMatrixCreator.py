from scipy.sparse import dok_matrix
from idfCalculator import IDFCalculator
from sklearn.preprocessing import normalize
from tqdm import tqdm
import os
import pickle

class TermByDocumentMatrixCreator:
    def __init__(self, bag_of_words_by_document, dictionary, path_to_cached_term_by_document_matrix = "./backend/cache/term_by_document_matrix.pickle", idf = True):
        self.bag_of_words_by_document = bag_of_words_by_document
        self.dictionary = dictionary
        self.tokens_indeces_dict = {token : i for i, token in enumerate(list(dictionary.keys()))}
        self.documents_indeces_dict = {document: i for i, document in enumerate(list(bag_of_words_by_document.keys()))}
        self.path_to_cached_term_by_document_matrix = path_to_cached_term_by_document_matrix
        self.idf = idf

        if self.idf:
            self.idfCalculator = IDFCalculator(bag_of_words_by_document, dictionary)

        if os.path.getsize(self.path_to_cached_term_by_document_matrix) == 0:
            print("Couldn't find cached term by document matrix at {path_to_cached_term_by_document_matrix}. Creating new one from scratch...:(".format(path_to_cached_term_by_document_matrix = self.path_to_cached_term_by_document_matrix))
            self.create_term_by_document_matrix()
        else:
            print("Found and loaded cached term by document matrix from {path_to_cached_term_by_document_matrix} . If you want to recreate it, use create_term_by_document_matrix() method.".format(path_to_cached_term_by_document_matrix = self.path_to_cached_term_by_document_matrix))
            with open(self.path_to_cached_term_by_document_matrix, 'rb') as file:
                self.term_by_document_matrix = pickle.load(file)

    def create_term_by_document_matrix(self):
        self.term_by_document_matrix = dok_matrix((len(self.dictionary), len(self.bag_of_words_by_document)))

        for document, counter in tqdm(self.bag_of_words_by_document.items()):
            for token, count in counter.items():
                row = self.tokens_indeces_dict[token]
                col = self.documents_indeces_dict[document]
                if self.idf:
                    self.term_by_document_matrix[row, col] = count * self.idfCalculator.token_idf(token)
                else:
                    self.term_by_document_matrix[row, col] = count
        
        self.term_by_document_matrix = normalize(self.term_by_document_matrix, axis = 0).tocsr()

        with open(self.path_to_cached_term_by_document_matrix, 'wb') as file:
            pickle.dump(self.term_by_document_matrix, file)
            print("Saved term by document matrix to cache at {path_to_cached_term_by_document_matrix}".format(path_to_cached_term_by_document_matrix = self.path_to_cached_term_by_document_matrix))