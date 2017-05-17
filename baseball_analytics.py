# -*- coding: utf-8 -*-
"""
Created on Sat May 1 20:38:34 2017

Project:  MLB Statistical Analysis

@author: Sanjai Syamaprasad
"""

import pandas as pd
import matplotlib.pyplot as plt
import folium
import seaborn as sns

years = list(range(2016,2017))

df_m = pd.read_csv('Master.csv')
df_f = pd.read_csv('Fielding.csv')
df_p = pd.merge(df_m, df_f, on='playerID', how='inner')
#df['range'] = df['range'].str.replace(',','-')

##Plotting years 2000-2016 using seaborn
for year in years:
    
    data = df_p[df_p.year == year] 

    h = sns.lmplot(x="weight", y="height", hue="bats",
           col="year", row = "POS", data=data);
    h.savefig("lm"+ str(year) +".png")              
              
    g = sns.jointplot(x="weight", y="height", data=data, kind="kde", color="m", col="year")
    g.plot_joint(plt.scatter, c="w", s=30, linewidth=1, marker="+")
    g.ax_joint.collections[0].set_alpha(0)
    g.set_axis_labels("Weight (lb)", "Height (in)");
    g.savefig("jp"+ str(year) +".png")
   
df_b = pd.read_csv('Batting.csv')

## inner joined 2 dataframes from Master.csv and Batting.csv based on playerID
df_c = pd.merge(df_m, df_b, on='playerID', how='inner')

#sorted based on year descending
df_s = df_c.sort_values(['yearID'], ascending=[False])

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

df_f = pd.read_csv('Fielding.csv')
df_p = df_c = pd.merge(df_m, df_f, on='playerID', how='inner')
