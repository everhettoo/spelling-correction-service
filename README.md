# Spelling Correction Service
This is a RestAPI for spelling correction implemented using FastAPI.

## Modules
- main.py - contains a simple REST API controller for processing the pipelines
- pipeline/* - contains the process pipelines for processing text
- models/* - contains models used for processing the text
- tests/* - contains tests for related modules

## Running the application
Pre-requisite: Python was installed and configured in the local machine.
- after cloning the code into local directory, locate into the dir: `cd spelling-correction-service`
- create virtual environment (to abstract pip installation): `python -m venv venv`
- activate the virtual environment (bash cmd): `source venv/bin/activate`
- install required libraries: `pip install -r requirements.txt`
- run the service: `python main.py`
- to read the service docs goto: http://localhost:8000/docs
