from bagOfWordsCreator import BagOfWordsCreator
from termByDocumentMatrixCreator import TermByDocumentMatrixCreator
from scipy.sparse import csr_matrix
from sklearn.preprocessing import normalize
from svdNoiseCanceler import SVDNoiseCanceler
import os
import numpy as np

class SearchHandler:
    def __init__(self, term_by_document_matrix_creator, no_responses, svd) -> None:
        self.no_responses = no_responses
        self.bag_of_words_creator = BagOfWordsCreator()
        self.term_by_document_matrix_creator = term_by_document_matrix_creator
        self.url_pattern = 'https://en.wikipedia.org/wiki/{article_name}'
        self.svd = svd

        if self.svd:
            self.svd_noise_canceler = SVDNoiseCanceler()
            self.svd_noise_canceler.load_svd_decomposition(self.term_by_document_matrix_creator.term_by_document_matrix)

    def search(self, phrase: str):
        cosine_norm = self.cosine_fit(phrase)

        documents_matching = [(cosine_norm[0, document_id], document) for document, document_id in self.term_by_document_matrix_creator.documents_indeces_dict.items()]

        documents_matching.sort(reverse = True)

        return [self.prepare_response(document, matching) for (matching, document) in documents_matching[:self.no_responses]]

    def cosine_fit(self, phrase: str):

        counter = self.bag_of_words_creator.create_bag_of_words_from_text(phrase)
        vector = csr_matrix((1, len(self.term_by_document_matrix_creator.tokens_indeces_dict.keys())))

        for token, count in counter.items():
            if token in self.term_by_document_matrix_creator.tokens_indeces_dict:
                col = (self.term_by_document_matrix_creator.tokens_indeces_dict[token])
                vector[0, col] = count
                            
        vector = normalize(vector)

        if self.svd:
            S_times_Vt = self.svd_noise_canceler.S_times_Vt
            U = self.svd_noise_canceler.U
            qU = vector @ U

            cosine_norm = qU @ S_times_Vt
        
        else:
            cosine_norm = vector @ self.term_by_document_matrix_creator.term_by_document_matrix 
        
        return cosine_norm
    
    def prepare_response(self, document, matching):
        base_name, extension = os.path.splitext(document)

        return {"title": " ".join(base_name.split('_')), "url": self.url_pattern.format(article_name = "_".join(base_name.split(' '))), "matching": round(matching, 2)}