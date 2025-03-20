# Spelling Correction Service
This is a RestAPI for spelling correction implemented using FastAPI. \

## Two stages in running the application:
1. Run the jupyter notebook for creating the corpus.
2. Run the main.py to load the corpus and host REST API endpoint at: http://localhost:8000/docs

## Running the application
Pre-requisite: Python was installed and configured in the local machine.
- after cloning the code into local directory, locate into the dir: `cd spelling-correction-service`
- create virtual environment (to abstract pip installation): `python -m venv venv`
- activate the virtual environment (bash cmd): `source venv/bin/activate`
- activate the virtual environment (windows): `venv\Scripts\activate`
- install required libraries: `pip install -r requirements.txt`
- download spacy corpus: `python -m spacy download en`
- run the `1-build-corpus.ipynb` to create corpus in `corpus/medical/medical.txt`
- run the `2-build-corpus-freq.ipynb` to create corpus in `corpus/medical_freq/medical_freq.tsv`
- run the `3-build-bigram-model.ipynb` to create corpus in `data/bigram_freq.pkl`
- run the service: `python 4-main.py`
- to read the service docs goto: http://localhost:8000/docs

## Modules
- main.py - contains a simple REST API controller for processing the pipelines
- pipeline/* - contains the process pipelines for processing text
- models/* - contains models used for processing the text
- tests/* - contains tests for related modules
