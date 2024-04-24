import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import porter
from nltk.corpus import stopwords
import re

nltk.download('punkt')
nltk.download('stopwords')

class Preprocessor:
    def __init__(self, language = "english"):
        self.language = language
        self.stemmer = porter.PorterStemmer()
        self.stopwords = {self.stemmer.stem(word) for word in stopwords.words(language)}
    
    def tokenize(self, text):
        return word_tokenize(text = text, language = self.language)
    
    def remove_punctuaction(self, text):
        return re.sub(r'[^\w\s]', ' ', text)

    def stem(self, tokens):
        return list(map(lambda token: self.stemmer.stem(token), filter(lambda token: len(self.stemmer.stem(token)) > 2 and self.stemmer.stem(token) not in self.stopwords, tokens)))

    def preprocess(self, text):
        return self.stem(self.tokenize(self.remove_punctuaction(text)))
