# -*- coding: utf-8 -*-
"""
Created on Sat May 1 20:38:34 2017
Project:  MLB Statistical Analysis
@author: Sanjai Syamaprasad
"""

import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pandas as pd
import re
import folium

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



df_m = pd.read_csv('Master.csv')
df_b = pd.read_csv('Batting.csv')


## inner joined 2 dataframes from Master.csv and Batting.csv based on playerID
df_c = pd.merge(df_m, df_b, on='playerID', how='inner')

#sorted based on year descending
df_s = df_c.sort_values(['yearID'], ascending=[False])

##Plotting years 2000-2016
#ScatteredPlot of Height VS Weight
for year in years:
    data = df_s[df_s.yearID == year] 
    df_sm = df_s[df_s.birthCountry == 'USA']
    plt.scatter(data['weight'], data['height'], alpha=0.5)
    plt.title("Height VS Weight for MLB players in "+ str(year))       #Title for plot
    plt.xlabel('Weight (lb)')                     #Label for x-axis
    plt.ylabel('Height (inches)')                   #Label for the y-axis
    plt.show()
#Histogram of Height by Year
    plt.hist(data['height'], facecolor='green',alpha=0.5)
    plt.title("Histogram of Height for MLB players in " + str(year))
    plt.xlabel("Height (in)")
    plt.ylabel("# of MLB players")
    plt.show()


##Shading chloropleth based on frequency of baseball players born in a USA
lst= []
states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
df_s['freq'] = df_s.groupby('birthState')['birthState'].transform('count')

for state in states:
    if any(df_s.birthState == state):
       lst.append(df_s.loc[df_s['birthState'] == state, 'freq'].iloc[0])
    else:
        lst.append(0)
#checking for Puerto Rico       
lst.append((df_s['birthCountry'] == "P.R.").sum())
states.append("PR")


frequency_states = [('birthState', states),
         ('freq', lst)]
df_freq = pd.DataFrame.from_items(frequency_states)


stateMap = folium.Map(location=[41, -97], zoom_start=4)
stateMap.choropleth(geo_path="state4.json",
                     fill_color='YlOrRd', fill_opacity=0.5, line_opacity=0.5,
                     data = df_freq,
                     key_on='feature.properties.STUSPS10',
                     columns = ["birthState","freq"]
                     ) 
stateMap.save(outfile='stateMLB.html')

