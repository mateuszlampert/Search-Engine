from sklearn.utils.extmath import randomized_svd
from sklearn.preprocessing import normalize
import numpy as np
import os
import pickle

class SVDNoiseCanceler:
    def __init__(self, rank = 3000, path_to_cached_svd_s_times_vt = "./backend/cache/svd_s_times_vt.pickle", path_to_cached_svd_u = "./backend/cache/svd_u.pickle"):
        self.rank = rank
        self.path_to_cached_svd_s_times_vt = path_to_cached_svd_s_times_vt
        self.path_to_cached_svd_u = path_to_cached_svd_u

    def initialize_svd_decomposition(self, term_by_document_matrix):
        U, S, Vt = randomized_svd(term_by_document_matrix, self.rank)
        S = np.diag(S)

        self.U = normalize(U, axis = 1)
        self.S_times_Vt = normalize(S @ Vt, axis = 0)

        with open(self.path_to_cached_svd_s_times_vt, 'wb') as file:
            pickle.dump(self.S_times_Vt, file)
        with open(self.path_to_cached_svd_u, 'wb') as file:
            pickle.dump(self.U, file)

    def load_svd_decomposition(self, term_by_document_matrix):
        if os.path.getsize(self.path_to_cached_svd_s_times_vt) == 0:
            print("Couldn't find cached SVD S @ T matrix at {path_to_cached_svd_s_times_vt}. Starting SVD decomposition from scratch...:(".format(path_to_cached_svd_s_times_vt = self.path_to_cached_svd_s_times_vt))
            self.initialize_svd_decomposition(term_by_document_matrix)
        elif os.path.getsize(self.path_to_cached_svd_u) == 0:
            print("Couldn't find cached U matrix at {path_to_cached_svd_u}. Creating new one from scratch...:(".format(path_to_cached_svd_u = self.path_to_cached_svd_u))
            self.initialize_svd_decomposition(term_by_document_matrix)
        else:
            print("Found and loaded SVD decomposition. If you want to recreate it, use initialize_svd_decomposition() method.")
            with open(self.path_to_cached_svd_s_times_vt, 'rb') as file:
                self.S_times_Vt = pickle.load(file)
            with open(self.path_to_cached_svd_u, 'rb') as file:
                self.U = pickle.load(file)