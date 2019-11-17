#import libraries
import requests
from bs4 import BeautifulSoup
import time
import glob
import os
import pandas as pd
import numpy as np
import urllib
import csv
import codecs
import bs4
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer 
import num2word

#parse the html page by finding all the anchor tags to get the URLs and store them in a list

def getlinks():
	links = []
	with open("urls.html", "r") as f:  
    	contents = f.read()
    	soup = BeautifulSoup(contents, 'lxml')  
    	for a_tag in soup.find_all("a"):
        	links.append(a_tag.text)

    #create a dataframe of the URLs
	df_links = pd.DataFrame(links)
	#name the column
	df_links.columns = ["url"]
	# change the index from 0 to 1
	df_links.index = np.arange(1,len(df_links)+1)

    return df_links