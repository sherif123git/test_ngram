import os

class Predictor:
    def __init__(self, model, normalizer):
        """
        init task. Automatically called when the class is instantiated 
        accept a preloaded ngrammodel and normalizer instances
        """
        self.model = model
        self.normalizer = normalizer
        self.model.load()
        self.top_k = os.environ.get("TOP_K")
        
    def normalize(self, text):
        """ call normalizer from Normalizer class """
        textL = self.normalizer.normalize(text)
        return textL

    def map_oov(self):
        pass

    def predict_next(self, text, k):
        """ calls lookup and returns the top-k words sorted by probability """
        return self.model.lookup(text, k)

    def show_predictions(self, dict_words):
        """ Print the suggested words in the terminal """
        print(f"Predictions: ", end="")
        print(dict_words, sep=", ")

    def run(self):
        """ This functions runs after instantiating the class """
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
            self.show_predictions(dict_words)
            
if __name__ == "__main__":
    pass

