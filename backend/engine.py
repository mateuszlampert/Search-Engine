from dictionaryCreator import DictionaryCreator
from termByDocumentMatrixCreator import TermByDocumentMatrixCreator
from searchHandler import SearchHandler

class Engine():
    def __init__(self, no_articles: int = 10, svd: bool = True, idf: bool = True):
        self.no_articles = no_articles
        self.svd = svd
        self.idf = idf

        self.dictionary_creator = DictionaryCreator()
        self.term_by_document_matrix_creator = TermByDocumentMatrixCreator(self.dictionary_creator.bag_of_words_by_document, self.dictionary_creator.dictionary, idf = idf)
        self.search_handler = SearchHandler(self.term_by_document_matrix_creator, self.no_articles, svd)

    def search(self, phrase: str) -> list[str]:
        return self.search_handler.search(phrase)
    
    def reset(self):
        pass