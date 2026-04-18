## env file contents
TRAIN_RAW_DIR=data/raw/train
EVAL_RAW_DIR=data/raw/eval
TRAIN_TOKENS=data/processed/train_tokens.txt
EVAL_TOKENS=data/processed/eval_tokens.txt
MODEL=data/model/model.json
VOCAB=data/vocab/vocab.json
UNK_THRESHOLD=3
TOP_K=3

## Project title and description
python implementation for a word prediction game in which a group of books is read and analysed.
ngram probability tables are created based on these books
for new words/statements that the user writes, these tables are searched to find the next suggested word

## Requirements
python version = 3.8.2
install the dependencies as shown in the requirements.txt file

## Setup
Follow these steps to get your development environment running:
clone the repo
install dependences
populate config/.env
download new text files into the correct folders

## Project structure
