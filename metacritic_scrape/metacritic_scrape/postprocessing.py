import json
import pandas as pd

f=open('./meta.json')
data = json.load(f)

df = pd.concat([pd.DataFrame(i,index=[0]) for i in data],ignore_index=True)
df.sort_values('metascore',ascending=False).reset_index(drop=True)

df.to_csv('metacritic_data_0223.csv')