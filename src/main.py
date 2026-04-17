import sys
import os
from dotenv import load_dotenv
#import importlib.metadata
import argparse

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from data_prep.Normalizer import Normalizer
from model.ngram_model import NGramModel

def parse_step():
    parser = argparse.ArgumentParser()
    parser.add_argument('--step', type=str, help='Step name')
    args = parser.parse_args()
    if args.step:
        pass
    else:
        print("No step provided.")
        quit()
    return args.step

def data_prep():
    normalizer = Normalizer()
    normalizer.load(os.environ.get("TRAIN_RAW_DIR"))
    print(f"Status: {normalizer.status}")
    if(normalizer.status==False):
        print("Book list is empty, Exiting...")
        quit()
    normalizer.normalize()

def generate_model():
    print("Generating model .....")
    ngram_m = NGramModel()
    ngram_m.run()

if __name__ == "__main__":
    #version = importlib.metadata.version('python-dotenv')
    #print(f"python-dotenv version: {version}")
    step=parse_step()
    load_dotenv("config/.env")
    for key, value in os.environ.items():
        print(f"{key}: {value}")
    if(step == "dataprep"):
        data_prep()
        pass
    elif(step == "model"):
        generate_model()
    elif(step == "inference"):
        pass
    elif(step == "all"):
        data_prep()
        generate_model()
        pass
    else:
        print("Wrong step provided.")
        quit()

