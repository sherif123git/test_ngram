import sys
import os
from dotenv import load_dotenv
import importlib.metadata

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from data_prep.Normalizer import Normalizer

if __name__ == "__main__":
    #version = importlib.metadata.version('python-dotenv')
    #print(f"python-dotenv version: {version}")

    load_dotenv("config/.env")
    normalizer = Normalizer()
    normalizer.load(os.environ.get("TRAIN_RAW_DIR"))
    print(f"Status: {normalizer.status}")
    if(normalizer.status==False):
        print("Book list is empty, Exiting...")
        quit()
    normalizer.normalize()