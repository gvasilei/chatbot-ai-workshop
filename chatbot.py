
import random
import string
import logging
import nltk

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import WordNetLemmatizer
from pprint import pformat
from corpus_loader import CorpusLoader

logging.basicConfig(level=logging.INFO, filename='robo.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
nltk.data.path.append('./nltk_data')


class Robo:
    def __init__(self):
        self.corpusLoader = CorpusLoader()
        self.corpus = self.corpusLoader.load_corpus()
        self.input_sentences = list(self.corpus.keys())
        logging.debug(pformat(self.corpus))
    

        self.lemmer = WordNetLemmatizer()
        self.tfIdfVec = TfidfVectorizer(tokenizer=self.tokenize)
        self.similarity_threshold = 0.30

        # Keyword Matching
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
        return [self.lemmer.lemmatize(token) for token in tokens]

    # Tokenize, convert to lowercase, remove punctuation and then lemmatize
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
        return self.lemmatize(nltk.word_tokenize(text.lower().translate(str.maketrans('', '', string.punctuation))))

    def isGreeting(self, sentence):
        """
        Checks if the provided sentence is considered a greeting or not.

        Args:
            sentence(str): A user provided sentence that might be a greeting or not

        Returns:
            bool: True if the sentence is a greeting and False if not.
        """
        for word in sentence.split():
            if word.lower() in self.GREETING_INPUTS: return True
        return False

    def greet(self):
        """
        Returns one of the GREETING_RESPONSES at random
        """
        return random.choice(self.GREETING_RESPONSES)

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
        tfidf = self.tfIdfVec.fit_transform(self.input_sentences + [user_input])

        logging.info(self.tfIdfVec.get_feature_names())
        logging.info(tfidf.shape)

        vals = cosine_similarity(tfidf[-1], tfidf[:-1]).flatten()
        highest_similarity_idx = vals.argsort()[-1]
        highest_similarity = vals[highest_similarity_idx]

        if(highest_similarity <= self.similarity_threshold):
            return "I am sorry! I don't understand you"
        else:
            reply_key = self.input_sentences[highest_similarity_idx]
            logging.debug(self.corpus[reply_key])
            if len(self.corpus[reply_key]) > 1:
                return random.choice(self.corpus[reply_key])
            else:
                 return self.corpus[reply_key][0]


if __name__ == "__main__":
    print("ROBO: My name is Robo. I will answer your queries about various topics. ask for help if you want to know more. If you want to exit, type Bye!")
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
