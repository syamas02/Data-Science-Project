# -*- coding: utf-8 -*-
"""
Created on Sat May 1 20:38:34 2017
Project:  MLB Statistical Analysis
@author: Sanjai Syamaprasad
"""

import requests
from bs4 import BeautifulSoup
import csv
import matplotlib.pyplot as plt
import pandas as pd
import brewer2mpl
import numpy as np
import random as rand
import re


years = list(range(2000,2017))
print(years)

fname_dict      = dict()
lname_dict      = dict()
position_dict   = dict()
salary_dict     = dict()
player_info     = dict()
player_info2    = dict()
fname_list      = []
lname_list      = []
position_list   = []
salary_list     = []

fname           = []
lname           = []
playerID        = []
weight          = []
height          = []
bats            = []
throws          = []


for year in years:
    url = "http://www.spotrac.com/mlb/rankings/base/" + str(year)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    for i in range(1,101):
        tr_list = soup.find_all('tr')
        tr_list_split = tr_list[i].get_text().split()
        position = tr_list_split[len(tr_list_split)-2]
        if position == "Catcher" or position =="Shortstop":
            position_list.append(position)
            lname_list.append(tr_list_split[len(tr_list_split)-3])
            fname_list.append(tr_list_split[len(tr_list_split)-4])        
        else:
            pos_str = tr_list_split[len(tr_list_split)-3] + " " + tr_list_split[len(tr_list_split)-2]
            position_list.append(pos_str)
            lname_list.append(tr_list_split[len(tr_list_split)-4])
            fname_list.append(tr_list_split[len(tr_list_split)-5]) 
        salary_list.append(re.sub('[\$,]', '', tr_list_split[len(tr_list_split)-1]) )     
    copy_fname_list     = fname_list[:]
    copy_lname_list     = lname_list[:]
    copy_pos_list       = position_list[:]
    copy_sal_list       = salary_list[:]
    
    fname_dict[year]    = copy_fname_list
    lname_dict[year]    = copy_lname_list
    position_dict[year] = copy_pos_list
    salary_dict[year]   = copy_sal_list
    del fname_list[:]
    del lname_list[:]
    del position_list[:]
    del salary_list[:]

print(fname_dict.items())
df_m = pd.read_csv('Master.csv')
df_b = pd.read_csv('Batting.csv')


#print(data_df['weight'])

## inner joined 2 dataframes 
df_c = pd.merge(df_m, df_b, on='playerID', how='inner')

#sorted based on year descending
#df_s = df_c.sort(['yearID'], ascending=[False])
df_s = df_c.sort_values(['yearID'], ascending=[False])
set2 = brewer2mpl.get_map('Set2', 'qualitative', 6).mpl_colors


for year in years:
    data = df_s[df_s.yearID == year] 
    plt.scatter(data['weight'], data['height'], alpha=0.5)
    plt.title("Height VS Weight for MLB players in "+ str(year))       #Title for plot
    plt.xlabel('Weight (lb)')                     #Label for x-axis
    plt.ylabel('Height (inches)')                   #Label for the y-axis
    plt.show()

    plt.hist(data['height'], facecolor='green',alpha=0.5)
    plt.title("Histogram of Height for MLB players in " + str(year))
    plt.xlabel("Height (in)")
    plt.ylabel("# of MLB players")
    plt.show()



