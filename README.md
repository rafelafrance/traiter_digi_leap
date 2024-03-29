# The Digi-Leap Information Extraction Project ![CI](https://github.com/rafelafrance/traiter_label_babel/workflows/CI/badge.svg)

# This project is now part of the Digi-Leap project.

## All right, what's this all about then?
**Challenge**: Given images of herbarium specimen sheets extract data from the label. See the example image below.

## Steps to extract information from the image:
1. Locate the label in the image. In the example the label is in the lower left corner.
1. Determine if the label is handwritten, typewritten, or a combination.
1. Adjust the image to help with the next step. Crop, rotate, enhance contrast, remove snow, etc.
1. Optical Character Recognition (OCR) the image.
1. Adjust the text gotten from the OCR. Correct misspellings, odd characters, etc.
1. Parse the OCR text to extract information from the label. Information Extraction (IE) is a subfield of Natural Language Processing (NLP)
    1. Use spaCy rule based parsers.
    1. Use either spaCy or HuggingFace NLP neural networks.
    1. NOTE: The prototype code used an older method called "Stacked Regular Expressions". This code will be replaced.

<img src="assets/11783738.jpg" alt="Herbarium sample" height="600" width="400">

## Install
You will need to have Python 3.9 (or later) installed. You can install the requirements into your python environment like so:
```
git clone https://github.com/rafelafrance/traiter_digi_leap.git
cd traiter_digi_leap
optional: virtualenv -p python3.9 venv
optional: source venv/bin/activate
python3 -m pip install --requirement requirements.txt
python3 -m pip install git+https://github.com/rafelafrance/traiter.git@master#egg=traiter
```  

## Run
```
python3 traiter.py ... TODO ...
```

## Tests
Having a test suite is absolutely critical. The strategy I use is every new pattern gets its own test. Any time there is a parser error I add the parts that caused the error to the test suite and correct the parser. I.e. I use the standard red/green testing methodology.

You can run the tests like so:
```
cd /my/path/to/traiter_digi_leap
python -m unittest discover
```
