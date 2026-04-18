import os
import json
import re

class NGramModel:
    train_tokens=""
    train_tokens_words=[]
    ngram_order = os.environ.get("NGRAM_ORDER")
    vocab = {}
    vocab_prob = {}
    ngram_all = {}
    def build_vocab(self, token_file):
        with open(token_file) as f:
            train_tokens = f.read()
            self.train_tokens_words = train_tokens.split()
        for word in self.train_tokens_words:
            if word in self.vocab:
                # increase the count by 1 if it already exists
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
    def generate_ngrams(self, filetextwords, n=2):
        
        # 2. Build the n-grams
        # stop at len(words) - n + 1 to avoid going out of bounds
        ngrams = [tuple(filetextwords[i:i + n]) for i in range(len(filetextwords) - n + 1)]
        
        # 3. Create the frequency table
        #ngram_table = Counter(ngrams)
        
        #return ngram_table
        return ngrams

    def build_counts_and_probabilities(self):
        st="he went to school and he went to the club and he went to his house" 
        self.train_tokens_words = st
        print(self.generate_ngrams(st.split(), 2))
        print(self.generate_ngrams(st.split(), 3))

        # Calculate the number of occurence --------------------------------------
        for n in range(1, int(os.environ.get("NGRAM_ORDER"))+1):
        #for n in range(2, 3):
            ngram=f"{n}ngram"
            self.ngram_all[ngram] = {}
            table=self.generate_ngrams(self.train_tokens_words.split(), n)
            for tupleitem in table:
                word = " ".join(tupleitem)
                print(word)
                if word in self.ngram_all[ngram]:
                    # increase the count by 1 if it already exists
                    self.ngram_all[ngram][word] = self.ngram_all[ngram][word]+1
                else:
                    # add the word if it does not exist
                    self.ngram_all[ngram][word] = 1
        print(self.ngram_all)

        # Calculate the probabilities --------------------------------------
        for n in range(int(os.environ.get("NGRAM_ORDER")), 1, -1):
            ngram=f"{n}ngram"
            ngram_p=f"{n-1}ngram"
            for sentence in self.ngram_all[ngram]:
                ngram_p_key=sentence.rsplit(' ', 1)[0] # remove the last word
                self.ngram_all[ngram][sentence] = self.ngram_all[ngram][sentence]/self.ngram_all[ngram_p][ngram_p_key]
        # calculate probability for 1ngram
        count = sum(list(self.ngram_all["1ngram"].values()))
        print(count)
        for word in self.ngram_all["1ngram"]:
            self.ngram_all["1ngram"][word] = self.ngram_all["1ngram"][word]/count
        print(self.ngram_all)

    def lookup(self):
        pass

    def save_model(self, model_path):
        with open (model_path, "w") as fw:
            json.dump(self.ngram_all, fw, indent=4)

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
        self.save_model(os.environ.get("MODEL"))

if __name__ == "__main__":
    # st="he went to school and he went to the club and he went to his house" 
    # self.train_tokens_words = st
    # print(self.generate_ngrams(st.split(), 2))
    # print(self.generate_ngrams(st.split(), 3))
    # ngram_m = NGramModel()
    # ngram_m.run()
    pass