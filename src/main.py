import sys
import os
from dotenv import load_dotenv
#import importlib.metadata
import argparse

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from data_prep.Normalizer import Normalizer

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

if __name__ == "__main__":
    #version = importlib.metadata.version('python-dotenv')
    #print(f"python-dotenv version: {version}")
    step=parse_step()
    load_dotenv("config/.env")
    if(step == "dataprep"):
        data_prep()
        pass
    elif(step == "model"):
        pass
    elif(step == "inference"):
        pass
    elif(step == "all"):
        data_prep()
        pass
    else:
        print("Wrong step provided.")
        quit()

