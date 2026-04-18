import os

class Predictor:
    def __init__(self, model, normalizer):
        self.model = model
        self.normalizer = normalizer
        self.model.load()
        self.top_k = os.environ.get("TOP_K")
        
    def normalize(self, text):
        textL = self.normalizer.lowercase(text)
        return textL

    def map_oov(self):
        pass

    def predict_next(self, text, k):
        return self.model.lookup(text, k)
        pass

    def show_predictions(self, dict_words):
        print(f"Predictions: ", end="")
        print(dict_words, sep=", ")

    def run(self):
        # show top words at the beginning
        dict_words = self.predict_next("", self.top_k)
        self.show_predictions(dict_words)
        while True:
            text=input()
            if text=="":
                continue
            if text=="quit":
                print("quitting...")
                quit()
            
            text = self.normalize(text)
            dict_words = self.predict_next(text, self.top_k)
            

