import os
import json

class NGramModel:
    train_tokens=""
    train_tokens_words=[]
    ngram_order = os.environ.get("NGRAM_ORDER")
    vocab = {}
    vocab_prob = {}
    def build_vocab(self, token_file):
        with open(token_file) as f:
            train_tokens = f.read()
            train_tokens_words = train_tokens.split()
        for word in train_tokens_words:
            if word in self.vocab:
                # increase the count by 1 if already exists
                self.vocab[word] = self.vocab[word]+1
            else:
                # add the word if it does not exist
                self.vocab[word] = 1
        # remove elements that appeared fewer than UNK_THRESHOLD
        UNK_THRESHOLD = int(os.environ.get("UNK_THRESHOLD"))
        for k in list(self.vocab.keys()):
            if(self.vocab[k]<UNK_THRESHOLD):
                del self.vocab[k]

        # for index, (k, v) in enumerate(self.vocab):
        #     self.vocab_prob[v] = v/len(self.vocab)
        
        # with open (os.environ.get("MODEL"), "w") as fw:
        #     jsonfile = json.dumps(vocab)
        #     fw.write(jsonfile)

    def build_counts_and_probabilities(self):
        pass

    def lookup(self):
        pass

    def save_model(self, model_path):
        pass

    def save_vocab(self, vocab_path):
        with open (vocab_path, "w") as fw:
            jsonfile = json.dumps(list(self.vocab))
            fw.write(jsonfile)
        # for debugging
        with open (vocab_path+".tmp", "w") as fw:
            jsonfile = json.dumps(self.vocab)
            fw.write(jsonfile)


    def load(self, vocab_path):
        pass

    def run(self):
        self.build_vocab(os.environ.get("TRAIN_TOKENS"))
        self.save_vocab(os.environ.get("VOCAB"))
        self.build_counts_and_probabilities()