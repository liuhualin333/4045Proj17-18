CZ4045 Natural Language Processing Project 1 README

- Contributors:
  
  Chen Hailin
  Deng Yue
  Liu Hualin
  Shi Ziji

— Dependencies:

  Python 3.6
  BeautifulSoup 4
  nltk
  sklearn
  scikit-learn

— Third-party Libraries Commands:

  BeautifulSoup 4:  pip install bs4
  nltk:             pip install nltk
  sklearn:          pip install sklearn
  scikit-learn:     pip install scikit-learn 
  
  OR
  
  pip install -U -r requirements.txt

- Dataset Download Link

  Dataset post link: https://github.com/liuhualin333/4045Proj17-18/blob/master/posts/all_posts.csv

  Dataset answer link: https://github.com/liuhualin333/4045Proj17-18/blob/master/posts/all_answers.csv

  Annotated post link: https://github.com/liuhualin333/4045Proj17-18/blob/master/posts/posts_training_clean_Annotated.txt

  Annotated answer link: https://github.com/liuhualin333/4045Proj17-18/blob/master/posts/answers_training_clean_Annotated.txt

— Installation Guide

  1. Download third party libraries according to previous instruction.
  2. Download datasets to data/ folder according to previous instruction.
  3. Navigate to code/ folder:
  4. Run the following command to tokenize all sentences in dataset:
        python tokenizer.py ../data/all_post_clean.csv ../data/all_answers_clean.csv
  5. Run the following command to:
        python 
  6. Run the following command to compute the top 4 keywords in all question posts data:
        python application.py

- Explainations

  all_posts.csv:                  contains data from all question posts
  all_answers.csv:                contains data from all answers posts
  
  all_posts_clean.csv:            contains all question posts which remove tags        
  all_answers_clean.csv:          contains all answers posts which remove tags
  
  posts_training.csv:             contains training data from question posts
  answers_training.csv:           contains training data from answers posts
  
  posts_traning_annotated.csv:    contains all annotated training data from question posts
  answers_training_annotated.csv: contains all annotated training data from answers posts
  
  all_posts_top_4_keywords:       contains top 4 keywords of all question posts
