
import random
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import nltk
from nltk.stem import WordNetLemmatizer

import logging
from pprint import pformat
logging.basicConfig(level=logging.INFO)

nltk.data.path.append('./nltk_data')

from corpus_loader import CorpusLoader

class Robo:
    def __init__(self):
        
        # Initialization method for Robo. Here you should create any object variables that you might need.
        self.corpusLoader = CorpusLoader()
        self.corpus = self.corpusLoader.load_corpus()
        self.input_sentences = list(self.corpus.keys())
        
        self.GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
        self.GREETING_RESPONSES = ("hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me")

    
    
    def lemmatize(self, tokens):
        """
        Lemmatizes a list of words / tokens. Takes as input the list of words and after lemmatizing each one returns a new list with the result.

        Args:
            tokens(:obj:`list` of :obj:`str`): List of words to be lemmatized

        Returns:
            (:obj:`list` of :obj:`str`): A list of lemmatized words
        """

        # Hint - Check the WordNetLemmatizer class on http://www.nltk.org/api/nltk.stem.html#module-nltk.stem.wordnet

        return []
    
    
    
    def tokenize(self, text):
        """
        Splits (tokenizes) a text into discreet words. Apart from the tokenization it applies some pre and post processsing

        Pre-processing: convert text to lowercase, remove any punctuation
        Post-processing: lemmatize each token.

        Args:
            text(str): the input text
        
        Returns:
            (:obj:`list` of :obj:`str`): a "bag of words"
        """

        # Hint - Use https://kite.com/python/docs/nltk.word_tokenize for splitting a text into distinct words

        return []

    
    
    def isGreeting(self, sentence):
        """
        Checks if the provided sentence is considered a greeting or not.

        Args:
            sentence(str): A user provided sentence that might be a greeting or not

        Returns:
            bool: True if the sentence is a greeting and False if not.
        """

        # Hint - Check if any of the words in the provided sentence is in the GREETING_INPUTS list.
        return False

    
    
    def greet(self):
        """
        Returns one of the GREETING_RESPONSES at random
        """
        return ""


    def help(self):
        return """I like telling jokes, gossip and chat in general. I'm pretty knowledgeable about the following topics:

        * AI
        * Bots
        * Computers
        * Food
        * History
        * Literature
        * Money
        * Movies
        * Politics
        * Psychology
        * Science
        * Sports
        * Trivia
        """


    
    def get_response(self, user_input):
        """
        Takes user input and tries to retrieve an appropriate response.
            
        Args:
            user_input (str): The user input :)

        Returns:
            str: The response to give to the user
        """

        # The TF / IDF algorithm, described in the presentation should be used here. Check the following class:
        # https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html and its method fit_transform
        # 
        # What we want to do here is to convert all potential input sentences into vertices. 
        # Then compare the similarity of them with the vertex that represents the actual user input.
        # The following method that can be used to calculate the similarity between vertices:
        #
        # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html
        
        return ""



if __name__ == "__main__":
    print("ROBO: My name is Robo. I will answer your queries about various topics. Type 'help' if you want to know more. If you want to exit, type Bye!")
    robo = Robo()

    while(True):
        try:
            user_input = input().lower()

            if user_input == 'bye':
                print("ROBO: Bye! take care..")
                break
            elif user_input == 'help':
                print("ROBO: "+robo.help())
            elif user_input == 'thanks' or user_input == 'thank you':
                print("ROBO: You are welcome..")
            elif robo.isGreeting(user_input):
                print("ROBO: "+robo.greet())
            else:
                print("ROBO: "+robo.get_response(user_input))
 
        except(KeyboardInterrupt, SystemExit):
            break
