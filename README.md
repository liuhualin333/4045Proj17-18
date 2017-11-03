# CZ4045 Natural Language Processing Project

## Introduction

This serves as partial fulfillment to course CZ4045 : Natural Language Processing in Nanyang Technological University, Singapore.

We developed two tokenizers on Stack Overflow posts. One is based on regular expression, and the other is based on Conditional Random Field (CRF).

The difficulty in tokenizing Stack Overflow data is that its content is highly unstructured, composing of both English text and code snippet. The tokenizer designed and developed by the team is capable to

    1. tokenize the code section into smaller meaningful units
    2. identify irregular name entities such as "Albert Einstein"
    3. identify file path like "src/main/resources"

which greatly improved the accuracy of tokenization, thus enhanced the performance of further analysis.

In the end, our CRF-based tokenizer achieved f1 score of 0.9483 on 5-fold cross validation, and regex-based tokenizer achieved f1-score of 0.9653.

## Contributors:

  Chen Hailin @Chen-Hailin , Deng Yue @spenceryue97 , Liu Hualin @liuhualin333 , Shi Ziji @stevenshi-23

## Dependencies:
 We have tested our program on python 3.


## Third-party Libraries Commands:(use pip3 install if default is python 2.7 pip)

  BeautifulSoup 4:  pip install bs4
  matplotlib        pip install matplotlib   
  nltk:             pip install nltk
  numpy:            pip install numpy
  scipy:            pip install scipy
  scikit-learn:     pip install scikit-learn 
  sklearn:          pip install sklearn
  sklearn_crfsuite: pip install sklearn_crfsuite 

  OR
  ```bash
  pip install -U -r requirements.txt
  ```

  
## Dataset Download Link
- Please download the data folder and put it under Root
  
  [Data folder](https://drive.google.com/open?id=1Na1gK7uqZkhbiwmi1DWThBBmUhrkzNwH)

  [Dataset post link](https://drive.google.com/open?id=190DqYXS8wDPmAB2UM20vHSOKUiRN0fNW)

  [Dataset answer link](https://drive.google.com/open?id=1CcssLW8sSC-KE_sAflbXk93d6ZbxpYGj)

  [Annotated post link](https://drive.google.com/open?id=0B1rcXBqgX69sbGZpUTZobk5hcDQ)

  [Annotated answer link](https://drive.google.com/open?id=0B1rcXBqgX69sbTB3SFVaVXItWFE)

# Installation Guide

  1. Download *python3* and third party libraries according to previous instruction.
  2. Run the following command open python interpreter:
     ``` python ```
     Then, run the following commands to download nltk resources:
  ```python
        import nltk
        nltk.download('stopwords')
        nltk.download('averaged_perceptron_tagger')   
  ```
     Last, press ctrl + Z to exit.
  3. Download datasets and put it into Data/ folder according to link given.
  4. Navigate to SourceCode/ folder:
  5. Run the following command to tokenize all sentences in dataset:
        ``` python3 tokenizer.py ```
  6. Run the following command and follow program instruction to run stemmer and POS tagging:
        ``` python3 nltk_controller.py ```
  7. Run the following command to compute the top 4 keywords in all question posts data:
        ``` python3 application.py ```

# Explanations of data
  
  all_posts_clean.txt:            contains all question posts which remove tags        
  all_answers_clean.txt:          contains all answers posts which remove tags
  
  posts_training_clean.txt:             contains training data from question posts with tags removed
  answers_training_clean.txt:           contains training data from answers posts with tags removed
  
  posts_manual_tokenized.txt:    contains all annotated training data from question posts
  answers_manual_tokenized.txt: contains all annotated training data from answers posts
  
  all_posts_top_4_keywords.txt:   contains top 4 keywords of all question posts

# Explanations of sourcecode
  
  application.py                  main application
  nltk_controller.py              use nltk package to do stemming, pos-tagging and section
                                  3.4
  tokeniser.py                    take a “clean“ version of dataset and tokenise both code
                                  and text
  utilities.py                    utility functions which can be used among scripts
  evaluation.py                   evaluation helper function

# Performance Summery
    Results on our annotated corpus:
    
    |                    | precision |   recall | f1-score |
    |--------------------|-----------|----------|----------|
    |    Regex tokenizer |    0.9578 |   0.9729 |   0.9653 |
    |      CRF tokenizer |    0.9478 |    0.949 |   0.9483 |
