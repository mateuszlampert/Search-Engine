# Search engine
### Author: Mateusz Lampert
### Computational methods for Science and Technology

# 1. Requirements

All the dependencies you need to install are mentioned in file <b>requirements.txt</b>. The most important libraries used for the algorithm are listed below:

- Algorithm:
    - numpy
    - scipy
    - sklearn
    - wikipeda
    - threading
    - nltk

# 2. Dataset

The dataset used for the search engine contains of about <b>50 000</b> articles crawled from <a href="https://www.wikipedia.org/">Wikipedia</a>. For crawling I used ready-made python library <a href="https://pypi.org/project/wikipedia/">wikipedia</a> with a custom crawler running on multiple threads. The crawler is located in file <b>crawler.ipynb</b>. All the articles were crawled in <b>simple english</b> version. Due to some computational limitations (more details in <b>section 4</b>), after filtering out some tokens, it resulted in final dictionary with about <b>50 000</b> tokens. The proccess of crawling took approximately about 13 hours. Initially, the dataset was meant to focus on focus on broadly understood culture and entertainment, however, finally the dataset contains full range of topics.

# 3. Data preprocessing

Code related to data preprocessing is located in file <b>preprocessor.py</b>.

Data preprocessing was based on three stages:

- removing punctuaction from the text
- stemming the text (<b>Porter Stemmer</b> from <b>nltk</b> module was used here). During this step all words ale simplified and all the stopwords and words shorter than 3 letters are filtered out, too.
- tokenization (<b>word_tokenize</b> from <b>nltk</b> modue was used here) of the text

# 4. Creating dictionary

Creating a dictionary of all words is connected with creating bag of words for each document (more details in <b>section 5</b>). The class responsible for the proccess of creating a dictionary of tokens is located in file <b>dictionaryCreator.py</b>.

Creating the dictionary also uses class in file <b>bagOfWordsCreator.py</b>, which returns <b>Counter</b> of tokens (for each token, we count number of occurrences in the text/file we passed as an argument). Text passed to the <b>BagOfWordsCreator</b> are preproccessed with the preprocessor mentioned in <b>section 3</b>.

During the proccess of creating dictionary, we create a bag of words for each article (and save to a dictionary of counters by documents - it is used for creating <b>term by document matrix</b>, more details in <b>section 5</b>) and add it to global counter representing the dictionary.

Due to some computational limitations, I decided to filter out all the tokens that are mentioned less than <b>8 times</b> among all articles (minimum number of occurrences is a parameter). Thanks to this, <b>approximately 75% of tokens</b> got filtered out and we got rid of uncommon words. The final dictionary contains about <b>50 000 tokens</b>.

# 5. Term by document matrix

The class responsible for creating a term by document matrix is located in file <b>termByDocumentMatrixCreator.py</b>.

During the proccess of creating the matrix, we use dedicated library for sparse matrices. To be more precise, <b>scipy.sparse</b> module with <b>dok_matrix</b> and <b>csr_matrix</b> were used. As initialization of csr_matrix and filling it with some many values turned out to be really time consuming, I decided to initialize dok_matrix and then convert it to csr_matrix. It resulted in approximately <b>50 times faster</b> matrix initialization. 

As we want the matrix to be the following data representation:

- rows denote tokens
- columns denote documents,

during the initialization of the TermByDocumentMatrixCreator we index all the tokens and documents, so we know rows and columns representing adequate tokens and documents, respectively.

One of the parameters for TermByDocumentMatrixCreator is <b>idf</b>. The user can decide whether he wants to use <b>IDF - Inverse Document Frequency</b> (more details on IDF in section <b>5.1</b> below). However, as it to recommended to use IDF for better performance, by default it is set to True.

The term by document matrix is then normalized along the columns.

## 5.1. IDF - Inverse Document Frequency

The class responsible for calculating IDF is located in file <b>idfCalculator.py</b>. To avoid calculating IDF multiple times, during initialization, we calculate it for each token in the dictionary and only read precalculated value later. During the proccess, for each token we calculate the value of:

$$IDF(t) = \log(\frac{N}{n_w})$$

where:

- $N$ - number of documents in total
- $n_w$ - number of docuements where token $t$ is present.

Using IDF significantly improves results as it reduces significance of common words.

# 6. SVD - low rank approximation

The class responsible for noise cancelling with low rank approximation is located in file <b>svdNoiseCanceler.py</b>. As a parameter, it takes rank (default value is set to rank = 3000, as it gave the best results).

Function used for SVD decomposition is <b>randomized_svd</b> from <b>sklearn.utils.extmath</b> module. The function returns decomposition to matrices $U, \Sigma, V^T$ and in my program is used in <b>initialize_svd_decomposition</b> method.

Theoretically, we should multiply matrices $U \times \Sigma \times V^T$ to receive matrix approximation with a given rank. However, even though we are using SVD decomposition function dedicated for sparse matrices, due to some computational limitations (.pickle file of $U$ matrix weighs approximately 1GB and my computer died when I tried to multiply the matrices), I was unable to multiply matrices $U \times \Sigma \times V^T$ and had to find computationally better approach. During initialization of the SVD decomposition I multiply matrices $\Sigma \times V^T$. Later on, when handling a request (more details in <b>section 7</b>), I multiply request vector $Q \times U$ and finally $ (Q \times U) \times (\Sigma \times V^T)$ (which is equal to $Q \times (U \times \Sigma \times V^T)$, but much more easier to compute). The only problem with the presented approach is matrix normalisation, as we should normalize $U \times \Sigma \times V^T$ and $Q$ separately, however, I used an approximation based on normalization of $U$ by rows and $\Sigma \times V^T$ by columns. It is not a perfect approximation of the norm as it happens to result in values higher than 1 (it should not happen when using cosine norm), but it is the best I could do with my equipment.

# 7. Handling requests

A class responsible for handling requests (located in file <b>searchHandler.py</b>) takes 3 parameters:

- Instance of TermByDocumentMatrixCreator used for creating TBD matrix
- expected number of responses
- information if an algorithm should use SVD

When <b>search</b> method is called on the SearchHandler it calculates cosine norm between vector $Q$ created from requested phrase (by creating bag of words for the phrase) and each document. Then, we take into account only the expected number of responses with the highest value. 

We normalize vector $Q$ and if we should use SVD we calculate matrix of cosine norm as $(Q \times U) \times (\Sigma \times V^T)$, otherwise, the result is just $Q \times A$

The class is also responsible for preparing the response in a format desired by the backend and frontend.

# 8. Engine

A class responsible for initialization of all the helper classes and communication with backend. An implementation is located in file <b>engine.py</b>.


# 9. Notes

As the initialization of all the classes and structures (all the structures weight approximately 3GB) takes much time, every significant structure is saved as a .pickle file so we can initialize the search engine faster. If user wants to reinitialize the structures, each class has dedicated method for that.

# 10. Summary

The algorithm gives us quite good results, we notice significant rise in the quality of responses while using SVD and IDF. 

I would consider using articles in English (not in simple english), as some of the articles in simple english are really short and do not contain many key words. The decision was made due to some time constraints and computational limitations.

# 11. Technology stack:

- Algorithm:
    - Python
- Backend:
    - Flask
- Frontend:
    - React