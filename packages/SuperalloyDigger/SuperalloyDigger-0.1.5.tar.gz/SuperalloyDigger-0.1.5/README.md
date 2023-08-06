
**SuperalloyDigger**
----------------------
Automatic extraction of chemical compositions and properties from the scientific literature of superalloy, covering specific chemical composition, density, γ' solvus temperature, solidus temperature, and liquidus temperature. Starting with a corpus of scientific articles scraped in XML, HTML or plain text format, NLP techniques are used to preprocess the raw archived corpus, followed by text classifier and table parser, named entity recognition, relation extraction of text and table, and dependency parser automatically. Finally, the extracted tuple entities containing article doi, alloy named entity, property specifier, property value, element and fraction, are compiled into a highly structured format for materials database.

This package is released under MIT License, please see the LICENSE file for details.

**Features**
----------------------
- Rule-based named entity recognition for superalloy.
- An automated data extraction pipeline for superalloy.
- Algorithm based on distance and number of entities, processing multiple relationship extraction without labeling samples.
- Table parser and table relation extraction algorithms to mine data from tables in documents.
- An interdependency parser to extract the information contain composition and property data simultaneous.

**Function**
----------------------
**Elsevier articles archive**

Automatically archive relevant articles from Elsevier journal
Combined with the CrossRef search Application Programming Interface (API),  Elsevier’s Scopus and Science Direct application programming interfaces (APIs) (https://dev.elsevier.com/), full text or abstract of corresponding field can be easily obtained. The premise is you have already got the copyright of the Elsevier database and applied for the APIkey of Elsevier. Users can find our source code at GitHub (https://github.com/MGEdata/SuperalloyDigger) to use this function locally. 

**Superalloy word embedding**

The word embedding model for superalloy corpus was pre-trained on ~9000 unlabeled full-text superalloy articles by Word2Vec continuous bag of words (CBOW) in genism(https://radimrehurek.com/gensim/), which use information about the co-occurrences of words by assigning high-dimensional vectors (embeddings) to words in a text corpus, to preserve their syntactic and semantic relationships.

**Superalloy property extractor**

Automatic extraction of properties from the scientific literature of superalloy, covering density, γ' solvus temperature, solidus temperature, and liquidus temperature.
Starting with a corpus of scientific articles scraped in XML or plain text format, NLP techniques are used to preprocess the raw archived corpus, followed by sentence classification, named entity recognition and relation extraction automatically. Finally, the extracted entities containing alloy named entity, property specifier and property value, are compiled into a highly structured format for materials database.

**Table information extractor and interdenpency parser**

Starting with a corpus of scientific articles scraped in XML, HTML or plain text format, NLP techniques are used to preprocess the raw archived corpus, followed by text classifier and table parser, named entity recognition, relation extraction of text and table, and dependency parser automatically. Finally, the extracted tuple entities containing article doi, alloy named entity, property specifier, property value, element and fraction, are compiled into a highly structured format for materials database.

**SuperalloyDigger Code**
----------------------
This code extracts data of property from TXT files. These TXT files need to be supplied by the researcher. The code is written in Python3. To run the code:

  1. Fork this repository
  2. Download the word embeddings model and configuration file
    - Available here: http://superalloydigger.mgedata.cn/#/home
  3. Download all files and place in the tableextractor/bin folder
  4. Place all necessary files in SuperalloyDigger/data folder for relation extraction, table information extraction, and dependency parse

**Usage**
----------------------
Clone this github repository and run
```
python3 setup.py install
```

Or simply use the code in your own project.

**License**
----------------------
All source code is licensed under the MIT license.

**Install**
----------------------
```
pip install superalloydigger
```
Note:The xlrd library version needs to be 1.2.0,run
```
pip install xlrd==1.2.0
```
If you don't have pip installed, you could also download the ZIP containing all the files in this repo and manually import the SuperalloyDigger class into your own Python code.
