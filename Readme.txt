CZ4045 Natural Language Processing Project 1 README

- Contributors:
  
  Chen Hailin
  Deng Yue
  Liu Hualin
  Shi Ziji

— Dependencies:

  Python 3.6
  BeautifulSoup 4
  matplotlib
  nltk
  numpy
  scipy
  scikit-learn
  sklearn
  sklearn_crfsuite

— Third-party Libraries Commands:

  BeautifulSoup 4:  pip install bs4
  matplotlib        pip install matplotlib   
  nltk:             pip install nltk
  numpy:            pip install numpy
  scipy:            pip install scipy
  scikit-learn:     pip install scikit-learn 
  sklearn:          pip install sklearn
  sklearn_crfsuite: pip install sklearn_crfsuite 
  
  OR
  
  pip install -U -r requirements.txt

- Dataset Download Link

  Dataset post link: https://drive.google.com/open?id=190DqYXS8wDPmAB2UM20vHSOKUiRN0fNW

  Dataset answer link: https://drive.google.com/open?id=1CcssLW8sSC-KE_sAflbXk93d6ZbxpYGj

  Annotated post link: https://drive.google.com/open?id=0B1rcXBqgX69sbGZpUTZobk5hcDQ

  Annotated answer link: https://drive.google.com/open?id=0B1rcXBqgX69sbTB3SFVaVXItWFE

— Installation Guide

  1. Download python3 and third party libraries according to previous instruction.
  2. Run the following command open python interpreter:
        python
     Then, run the following commands to download nltk resources:
        import nltk
        nltk.download('stopwords')
        nltk.download('averaged_perceptron_tagger')
     Last, press ctrl + Z to exit.
  3. Download datasets and put it into Data/ folder according to link given.
  4. Navigate to SourceCode/ folder:
  5. Run the following command to preprocess data:
        python data_processing.py
  5. Run the following command to tokenize all sentences in dataset:
        python tokenizer.py 
  6. Run the following command and follow program instruction to run stemmer and POS tagging:
        python nltk_controller.py
  7. Run the following command to compute the top 4 keywords in all question posts data:
        python application.py

- Explanations of data

  all_posts.txt:                  contains data from all question posts
  all_answers.txt:                contains data from all answers posts
  
  all_posts_clean.txt:            contains all question posts which remove tags        
  all_answers_clean.txt:          contains all answers posts which remove tags
  
  posts_training.txt:             contains training data from question posts
  answers_training.txt:           contains training data from answers posts
  
  posts_traning_annotated.txt:    contains all annotated training data from question posts
  answers_training_annotated.txt: contains all annotated training data from answers posts
  
  all_posts_top_4_keywords.txt:   contains top 4 keywords of all question posts

— Explanations of sourcecode
  
  application.py                  main application
  data_processing.py              clean all xml tags and output a “clean” version of 
                                  dataset
  evaluation.py                   calculate evaluation metrics
  nltk_controller.py              use nltk package to do stemming, pos-tagging and section
                                  3.4
  tokeniser.py                    take a “clean“ version of dataset and tokenise both code
                                  and text
  utilities.py                    utility functions which can be used among scripts
