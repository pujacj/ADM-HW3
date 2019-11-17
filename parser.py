import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
from collections import OrderedDict
import os
from pymongo import MongoClient
import json

### INFO BOX COLLECTION For First Data Set
dataFrame=pd.DataFrame(columns= ["Title","Intro","Plot","film_name","Directed by","Produced by","Written by",
                        "Starring","music","Based on","Cinematography","Productioncompany "
                        "Release date","Running time","Country","Language","Budget"])

noinfobox = []
data=requests.get("https://raw.githubusercontent.com/CriMenghini/ADM/master/2019/Homework_3/data/movies1.html")
soup = BeautifulSoup(data.text, 'html.parser')
liste = [sites.text for sites in soup.select('a')]
liste[:10]
dataframe=pd.DataFrame(liste)
dataframe["id"]= dataframe.index + 1
dataframe.rename(columns= {0 : "URL"},inplace=True)
columns=dataframe.columns.tolist()
dataframe = dataframe[columns[::-1]]
dataframe.head()
for i in dataframe.loc[:, "id"]:
    pages = OrderedDict()
    with open("./wikipages/wiki{}.txt".format(i), "rb") as f:
        text = f.read()
    soup1 = BeautifulSoup(text, "html.parser")
    pages = OrderedDict()
    try:
        for tr in soup1.find("table", {"class": "infobox vevent"}).find("tbody").find_all("tr"):
            for th in tr.find_all("th"):
                if not th.next_sibling:
                    pass
                elif th.next_sibling.name == "td":
                    pages[th.text] = th.next_sibling.text

        pages["URL"] = dataframe[dataframe["id"] == i]["URL"].values[0]
        pages["id"] = i
        pages["title"] = soup1.find("table", {"class": "infobox vevent"}).find("tbody").find("tr").find("th").text
        dataa = pd.DataFrame(pages, index=[0])
        dataFrame = dataFrame.append(dataa, ignore_index=True, sort=False)

    except AttributeError as e2:
        print("Film id number {} do not have infobox".format(i))
        noinfobox.append(i)



## PARSING FOR paragraph
title_data = []
intro_data = []
plot_data = []

for i in range(1, 10001):
    print(i)
    intro = ""
    plot = ""
    p1, p2, p3, p4, p5, p6, p7, p8 = "", "", "", "", "", "", "", ""
    with open("articles/article_{}.html".format(i), "r") as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'lxml')
        # find the title
        title = soup.find("title")
        title_data.append(title.string)

        # find the intro (check for maximum of 4 paragraphs under the intro section)
        entrysoup = soup.find('div', attrs={"class": "mw-parser-output"})
        try:
            for strong_tag in entrysoup.findAll('h2'):
                if (strong_tag.get_text() == "Plot[edit]") | (strong_tag.get_text() == "Plot summary[edit]"):
                    intro_para = strong_tag.find_previous_sibling('p')
                    try:
                        p1 = intro_para.text
                    except:
                        pass
                    try:
                        para_2 = p1.find_previous_sibling('p')
                    except:
                        pass
                    if not para_2:
                        pass
                    else:
                        p2 = para_2.text
                    try:
                        para_3 = para_2.find_previous_sibling('p')
                    except:
                        pass
                    if not para_3:
                        pass
                    else:
                        p3 = para_3.text
                    try:
                        para_4 = para_3.find_previous_sibling('p')
                    except:
                        pass
                    if not para_4:
                        pass
                    else:
                        p4 = para_4.text
        except:
            pass

        # find the plot (check for maximum of 4 paragraphs under the plot section)
        try:
            for strong_tag in entrysoup.findAll('h2'):
                if (strong_tag.get_text() == "Plot[edit]") | (strong_tag.get_text() == "Plot summary[edit]"):
                    plot_para = strong_tag.find_next_sibling('p')
                    try:
                        p5 = plot_para.text
                    except:
                        pass
                    try:
                        para_6 = p5.find_next_sibling('p')
                    except:
                        pass
                    if not para_6:
                        pass
                    else:
                        p6 = para_6.text
                    try:
                        para_7 = para_6.find_next_sibling('p')
                    except:
                        pass
                    if not para_7:
                        pass
                    else:
                        p7 = para_7.text
                    try:
                        para_8 = para_7.find_next_sibling('p')
                    except:
                        pass
                    if not para_8:
                        pass
                    else:
                        p8 = para_8.text
        except:
            pass
    intro = ', '.join(filter(None, (p4, p3, p2, p1)))
    intro_data.append(intro)
    plot = ', '.join(filter(None, (p5, p6, p7, p8)))
    plot_data.append(plot)