#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 16 07:04:52 2017

Project:  MLB Statistical Analysis

Webscrape http://www.spotrac.com/mlb/rankings/ for salary data
and compare with height of MLB player in CSV files.

@author: Sanjai Syamaprasad
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import seaborn as sns

years = list(range(2011,2017))

name_list       = []
position_list   = []
salary_list     = []
height_list     = []
playerID        = []
weight          = []
height          = []

df_m = pd.read_csv('Master.csv')

df_f = pd.read_csv('Fielding.csv')
df_p = df_c = pd.merge(df_m, df_f, on='playerID', how='inner')

df_p['fullName'] = df_p['nameFirst'] + df_p['nameLast']

    
df_y = df_p[df_p.birthYear > 1970]
df_y = df_y.sort_values(['birthYear'], ascending=[False])

## using Beautiful Soup to retrieve data of salaries
for year in years:
    url = "http://www.spotrac.com/mlb/rankings/" + str(year)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    for i in range(1,101):
        tr_list = soup.find_all('tr')
        tr_list_split = tr_list[i].get_text().split()
        position = tr_list_split[len(tr_list_split)-2]
        if position == "Catcher" or position =="Shortstop":
            position_list.append(position)
            name_str = tr_list_split[len(tr_list_split)-4] + tr_list_split[len(tr_list_split)-3]       
        else:
            pos_str = tr_list_split[len(tr_list_split)-3] + " " + tr_list_split[len(tr_list_split)-2]
            position_list.append(pos_str)
            name_str = tr_list_split[len(tr_list_split)-5] + tr_list_split[len(tr_list_split)-4]
            name_list.append(name_str)
        salary_list.append(int(re.sub('[\$,]', '', tr_list_split[len(tr_list_split)-1])))

    salary_list2=[]
    position_list2=[]
    for j in range(len(name_list)):
        for index, row in df_y.iterrows():
           if name_list[j] == row['fullName']:
                height_list.append(row['height'])
                salary_list2.append(salary_list[j])
                position_list2.append(position_list[j])
                break
    df_z = pd.DataFrame({'salary': salary_list2, 'height': height_list, 'position': position_list2})
    with sns.axes_style("white"):
        g=sns.jointplot(x="salary", y="height", data=df_z, kind="hex", color="k");
    g.fig.suptitle('year = '+str(year), fontsize=20,color="b",alpha=0.5)
    g.set_axis_labels("Salary (* $10,000,000)", "Height (in)");

    g.savefig("jpsal"+ str(year) +".png") 

    del name_list[:]
    del position_list[:]
    del position_list2[:]
    del salary_list[:]
    del salary_list2[:]
    del height_list[:]
    del tr_list[:]
    del tr_list_split[:]



