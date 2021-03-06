'''
Victor Sebastian Martinez
Youtube comment scraper

Usage: python <search_term> <number_of_comments>

For preprocessing:
https://towardsdatascience.com/nlp-for-beginners-cleaning-preprocessing-text-data-ae8e306bef0f

Issues:
If there are non-english comments, the desired number of comments could not be met
the isEnglish functions sometimes classifies english sentences as non-english

'''
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import time
import sys
import re
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer 
from selenium import webdriver
from langdetect import detect

def remove_emoji(string):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)

def isEnglish(sentence):
    return detect(sentence) == 'en'
    # try:
    #     sentence.encode(encoding='utf-8').decode('ascii')
    # except UnicodeDecodeError:
    #     return False
    # else:
    #     return True

def clean_comments(raw_comments):
    cleansed_comments = []
    for comment in raw_comments:
        if isEnglish(comment.text) and comment.text is not '' or comment.text is not ' ':
            # word_tokens = tokenizer.tokenize(comments[comment])
            # filtered_sentence = [w for w in word_tokens if not w in stop_words]
            # lem_text = [lemmatizer.lemmatize(i).lower() for i in filtered_sentence]
            # # stem_text = [stemmer.stem(i) for i in filtered_sentence]
            # f.write(' '.join(lem_text) + '\n')
            clean_comment = remove_emoji(comment.text)
            cleansed_comments.append(clean_comment)
    return  cleansed_comments

driver = webdriver.Firefox()

# Create directories
to_search = sys.argv[1]
cwd = os.getcwd()
absolute_test_dir = os.path.join(cwd, "Comments/")

try:
    os.makedirs(absolute_test_dir, exist_ok=True)
except OSError:
        print(f"Creation of {absolute_test_dir} directory failed")

# Search for a video
driver.get("https://www.youtube.com/results?search_query=" + to_search)
Video = driver.find_element_by_xpath("//div[@class='text-wrapper style-scope ytd-video-renderer']")
Video.click()
time.sleep(3)

# Search for comments
desired_comments = int(sys.argv[2])
comments = []
# comment_section = driver.find_element_by_xpath('//*[@id="comments"]')
MAX_COMMENTS = driver.find_element_by_xpath('//*[@class="count-text style-scope ytd-comments-header-renderer"]')
MAX_COMMENTS = int(MAX_COMMENTS.text.split()[0].replace(",", ""))

# Scroll down until desired number of comments are reached
desired_comments = MAX_COMMENTS if desired_comments > MAX_COMMENTS else desired_comments
while desired_comments > len(comments):
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(3)
    comments = driver.find_elements_by_xpath('//*[@id="content-text"]')

# Preprocess and save
stop_words = stopwords.words('english')
tokenizer = RegexpTokenizer(r"\w+(?:[-']\w+)*|'|[-.(]+|\S\w*") # \w - Any character, + - match one or more
lemmatizer = WordNetLemmatizer()

with open(absolute_test_dir + to_search + '.txt', 'w') as f:
    comments = clean_comments(comments)
    for cmt in range(desired_comments):
        comment = comments[cmt]
        f.write(comment + '\n')
driver.quit()