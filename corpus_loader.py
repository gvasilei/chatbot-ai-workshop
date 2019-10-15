import os
import io
import yaml
import glob

class CorpusLoader:
    def __init__(self, corpus_path='./corpus'):
        self.corpus_path = corpus_path

    def read_corpus(self, file_name):
        """
        Read and return the data from a corpus yaml file.
        """
        with io.open(file_name, encoding='utf-8') as data_file:
            return yaml.load(data_file, Loader=yaml.FullLoader)

    def list_corpus_files(self):
        """
        Return a list of file paths to each data file in the specified corpus.
        """
        paths = []

        if os.path.isdir(self.corpus_path):
            paths = glob.glob(self.corpus_path + '/**/*.yml', recursive=True)
        else:
            paths.append(self.corpus_path)

        paths.sort()
        return paths

    def load_corpus(self):
        """
        Return the data contained within a specified corpus.
        """
        corpus = {}

        data_file_paths = self.list_corpus_files()
        for file_path in data_file_paths:
            corpus_data = self.read_corpus(file_path)

            conversations = corpus_data.get('conversations', [])
            # A conversation is a list where the first element is the user input and the rest are potential answers
            for conversation in conversations:
                user_input = conversation[0].lower()

                if conversation[0] in corpus:
                    corpus[user_input] += conversation[1:]
                else:
                    corpus[user_input] = conversation[1:]
        
        return corpus