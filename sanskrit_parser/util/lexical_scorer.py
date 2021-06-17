'''
Scorer for lexical splits

Uses word2vec based scoring the splits. The splits are
passed through sentencepiece first to handle possibly unseen words

Requires sentencepiece to be installed

@author: avinashvarna
'''

import sys
import logging

from sanskrit_parser.util.data_manager import data_file_path

try:
    import sentencepiece as spm
    import gensim
    gensim_enabled = True
except ImportError:
    msg = 'gensim and/or sentencepiece not found. '
    msg += 'Lexical scoring will be disabled\n'
    msg += 'To enable scoring please install gensim and sentencepiece'
    logging.warning(msg)
    gensim_enabled = False


class Scorer(object):

    sentencepiece_file = "sentencepiece.model"
    word2vec_file = "word2vec_model.dat"

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        if gensim_enabled:
            self.sentencepiece_file = data_file_path(self.sentencepiece_file)
            self.sp = spm.SentencePieceProcessor()
            self.sp.Load(self.sentencepiece_file)
            self.word2vec_file = data_file_path(self.word2vec_file)
            self.model = gensim.models.Word2Vec.load(self.word2vec_file)

    def score_splits(self, splits):
        sentences = [" ".join(map(str, split)) for split in splits]
        return self.score_strings(sentences)

    def score_strings(self, sentences):
        if gensim_enabled:
            self.logger.debug("Sentence = %s", sentences)
            pieces = [self.sp.EncodeAsPieces(sentence) for sentence in sentences]
            self.logger.debug("Pieces = %s", pieces)
            scores = self.model.score(pieces, total_sentences=len(sentences))
            self.logger.debug("Score = %s", scores)
        else:
            # Use negative of length.
            # This will result in longer sentences getting a higher weight
            scores = [-len(sentence.split(' ')) for sentence in sentences]
        return scores


if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser(description='Lexical Scorer')
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('data', nargs="?", type=str, default=None)

    args = parser.parse_args()
    if args.debug:
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    else:
        logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    score = Scorer().score_strings([args.data])
    print("Input:", args.data)
    print("Score =", score)
