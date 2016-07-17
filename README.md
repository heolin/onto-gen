onto-gen
========
Module for generating ontologies based on text corpus.


I.  Preparing corpus.
    Current pipeline supports only pdf files. You can use different files by converting them into txt and placing in "corpus/txt" directory.

    Place pdf files into "corpus/pdf" directory.
    Use:
    make

    When whole process is ready, corpus file  will be placed in "corpus/final/final.txt".

II. Creating topics for Latent Semantic Indexing (LSI).

    1. Creating a dictionary
    ./topics/analyser.py -i INPUT-CORPUS-FILE

    This command will create dictionary file in the same directory as INPUT-CORPUS-FILE.
    INPUT-CORPUS-FILE is a file with corpus sentences listed one in each line.
    For example, corpus created in the previous section.

    2. Creating a LSI models:
    ./topics/models.py -i INPUT_PATH
    INPUT-PATH is a path to a dictionary created in the first step.
    This command will create LSI models in the same directory as dictionary.

III. Create inverted index

    1. Create index
    ./search/search_manager.py -c PATH-TO-SCHEMA -i PATH-TO-INDEX
    PATH-TO-INDEX is a path to directory where index will be created
    PATH-TO-SCHEMA is a path to schema file described below:
    Example schema format (means: store title, store full text, allow full text search):
    title	TEXT	True

    2. Read corpus files into index
    To read corpus file use:
    ./search/search_manager.py -i PATH-TO-INDEX -q -af PATH-TO-FILE
    PATH-TO-INDEX is a path to directory where index was created in previous step
    PATH-TO-FILE is a path to corpus file you want to read into index

III. Creating an ontology
    WARNING! All calculations for distance matrix are being stored in "./temp/" directory to speed up process in next generation,
    remember to clear (rm ./temp/*) this directory after changing INPUT-TERMS list.

    1. Creating new ontology
    ./ontology_factory.py -i INDEX-PATH -c CORPUS-PATH -t INPUT-TERMS -o OUTPUT-OWL-FILE
    Additionaly you can use -l option to lemmatize input terms.

    INDEX-PATH is a path to a directory in which inverted index was created in the previous section.
    CORPUS-PATH is a path to topic dictionary created in II section
    OUTPUT-OWL-FILE is a path for generated output OWL ontology
    INPUT-TERMS is a path to file with terms listed one in each line

    2. To extend existing ontology
    ./ontology_factory.py -i INDEX-PATH -c CORPUS-PATH -t INPUT-TERMS -o OUTPUT-OWL-FILE -g INPUT-OWL
    Additionaly you can use -l option to lemmatize input terms.

    INDEX-PATH is a path to a directory in which inverted index was created in the previous section.
    CORPUS-PATH is a path to topic dictionary created in II section
    OUTPUT-OWL-FILE is a path for generated output OWL ontology
    INPUT-TERMS is a path to file with terms listed one in each line
    INPUT-OWL is path to OWL file you want to extend

