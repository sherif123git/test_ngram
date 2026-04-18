import os
import json
import re
from collections import Counter

class NGramModel:
    train_tokens=""
    train_tokens_words=[]
    ngram_order = 0
    vocab = {}
    vocab_prob = {}
    ngram_all = {}

    def __init__(self):
        """ init task. Automatically called when the class is instantiated """
        self.ngram_order = int(os.environ.get("NGRAM_ORDER"))

    def build_vocab(self, token_file):
        """ build vocabulary list """
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
        """
        count all n-gram at orders 1 through NGRAM_ORDER and compute 
        MLE probabilities.
        """
        st="he went to school and he went to the club and he went to his house".split()
        #self.train_tokens_words = st
        #print(self.generate_ngrams(st, 2))
        #print(self.generate_ngrams(st, 3))

        # Calculate the number of occurence --------------------------------------
        for n in range(1, int(os.environ.get("NGRAM_ORDER"))+1):
            #print(f"n={n}")
        #for n in range(2, 3):
            ngram=f"{n}ngram"
            self.ngram_all[ngram] = {}
            table=self.generate_ngrams(self.train_tokens_words, n)
            for tupleitem in table:
                sentence = " ".join(tupleitem)
                #print(sentence)
                if(n==1):
                    if sentence in self.ngram_all[ngram]:
                        # increase the count by 1 if it already exists
                        self.ngram_all[ngram][sentence] = self.ngram_all[ngram][sentence]+1
                    else:
                        # add the sentence if it does not exist
                        self.ngram_all[ngram][sentence] = 1
                else:
                    sentence_t = sentence.rsplit(' ', 1)[0]
                    last_word = sentence.split()[-1]
                    if sentence_t in self.ngram_all[ngram]:
                        # increase the count by 1 if it already exists
                        if last_word in self.ngram_all[ngram][sentence_t]:
                            self.ngram_all[ngram][sentence_t][last_word] = self.ngram_all[ngram][sentence_t][last_word] +1
                        else:
                            self.ngram_all[ngram][sentence_t][last_word] = 1
                    else:
                        # add the sentence if it does not exist                        
                        self.ngram_all[ngram][sentence_t]={}
                        self.ngram_all[ngram][sentence_t][last_word] = 1

        #print(json.dumps(self.ngram_all, indent=4) )
        
        # Calculate the probabilities --------------------------------------
        for n in range(int(os.environ.get("NGRAM_ORDER")), 1, -1):
            ngram=f"{n}ngram"
            ngram_p=f"{n-1}ngram"
            for sentence_dict in self.ngram_all[ngram]:
                total = sum(list(self.ngram_all[ngram][sentence_dict].values()))
                for word in self.ngram_all[ngram][sentence_dict]:
                    #ngram_p_key=sentence.rsplit(' ', 1)[0] # remove the last word
                    self.ngram_all[ngram][sentence_dict][word] = self.ngram_all[ngram][sentence_dict][word]/total
        #print(json.dumps(self.ngram_all, indent=4) )

        # calculate probability for 1ngram
        count = sum(list(self.ngram_all["1ngram"].values()))
        print(count)
        for word in self.ngram_all["1ngram"]:
            self.ngram_all["1ngram"][word] = self.ngram_all["1ngram"][word]/count
        #print(self.ngram_all)

    def save_model(self, model_path):
        """ save the probability tables to model.json """
        with open (model_path, "w") as fw:
            json.dump(self.ngram_all, fw, indent=4)

    def save_vocab(self, vocab_path):
        """ save vocabulary list to vocab.json """
        with open (vocab_path, "w") as fw:
            jsonfile = json.dumps(list(self.vocab))
            fw.write(jsonfile)
        # for debugging
        with open (vocab_path+".tmp", "w") as fw:
            jsonfile = json.dumps(self.vocab)
            fw.write(jsonfile)


    def load(self):
        """ load json files during inference """
        with open(os.environ.get("VOCAB"), 'r', encoding='utf-8') as file:
            self.vocab = json.load(file)
        with open(os.environ.get("MODEL"), 'r', encoding='utf-8') as file:
            self.ngram_all = json.load(file)
        #print(self.ngram_all)
    
    def get_last_n_words(self, sentence, n):
        # Split the sentence into a list of words
        words = sentence.split()
        
        # Try to return n words, then n-1, down to 1
        for count in range(n, 0, -1):
            if len(words) >= count:
                # Join the last 'count' words back into a string
                return count, " ".join(words[-count:])
        
        return 0, "" # Return empty s

    def lookup(self, text, k):
        """ backoff lookup 
        try the highest-order context first, fall back to
        lower orders down to 1-gram
        return empty array if no match is found
        """
        sentence=text.strip()
        count = 0
        #words=[]
        # for n in range(self.ngram_order-1, 0, -1):
        count, textslice = self.get_last_n_words(sentence, self.ngram_order-1)
        if(count == 0):
            return []
        
        #print(f"Enough words found ({count})")

        ngram=f"{count+1}ngram"
        if textslice not in self.ngram_all[ngram]:
            return []
        avail_dict = self.ngram_all[ngram][textslice]
        top_k = int(os.environ.get("TOP_K"))
        # if(len(avail_dict)>=top_k):
        top_v = Counter(avail_dict).most_common(top_k)
        top_words = [item[0] for item in top_v]
        # else:
        return top_words

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