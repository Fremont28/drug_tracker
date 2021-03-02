#This script visualizes the price of prescription (legal) drugs on the website Drugs.com. 

#import required libraries 
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import re 
import numpy as np 
from datetime import datetime 
import requests 
import plotly.graph_objects as go

drug='Ambien' #enter the name of the prescription drug here (only change needed) **

url="https://www.drugs.com/price-guide/{}".format(drug)
page=requests.get(url)
soup=BeautifulSoup(page.content)
soup_div=soup.find_all('div')
soup_div1=soup.find_all('div',class_=re.compile('pricingFrom'))
soup_div1

drug_box=[]
for f in soup_div1:
    print(f.get_text()) 
    drug_box.append(f.get_text())

#convert the list of drug prices to a dataframe 
db1=pd.DataFrame(drug_box)
db1.columns=['col1']
db1['col1']=db1['col1'].apply(str)
db1['col1'] = db1['col1'].astype(str).replace('\.0', '', regex=True)
db1['col1'] = db1['col1'].astype(str).replace('\,', '', regex=True)
db1= pd.DataFrame(db1.col1.str.split('for',1).tolist(),
                                 columns = ['col1','col2'])

db1['col1']=db1.col1.str.extract('(\d+)')
db1['col2']=db1.col2.str.extract('(\d+)')
db1['col1']=db1['col1'].astype(int)
db1['col2']=db1['col2'].astype(int)
db1.columns=['price','tab_cnt']

#check if price >=$50000 or <$50000 
db1x=db1[db1.price>=5000]
db1x['price']=db1x['price'].astype(str).str[0:4]

db2x=db1[db1.price<5000]
db2x['price']=db2x['price'].astype(str).str[0:4]

db1=pd.concat([db1x,db2x],axis=0)
db1['price']=db1['price'].astype(int)
db1['price_tab']=db1.price/db1.tab_cnt #price per tablet 

#append dataframe to a csv file 
csv_name=datetime.today().strftime('%Y-%m-%d')
db1.to_csv(drug+csv_name)
file_name=drug+csv_name 

#import the csv file from a local folder 
d1= pd.read_csv(file_name, sep=",", header=None) 
d1.columns = ["col1", "price", "tab_cnt", "price_tab"]
headers = d1.iloc[0]

d1 = pd.DataFrame(d1.values[1:], columns=headers)
d2=d1.iloc[:,1:d1.shape[1]]
d2['drug']=drug 
d2['price']=d2['price'].astype(float)
d2['tab_cnt']=d2['tab_cnt'].astype(float)

d2=d2[["drug","price_tab","tab_cnt","price"]]
d2.columns=['drug','price/tab','tab_count','total_price']
d2=d2.drop_duplicates(keep="first")
d2['price/tab']=d2['price/tab'].astype(float)

f1= go.Figure(data=[go.Table(
    header=dict(values=list(d2.columns),
                fill_color='plum',
                align='left'),
    cells=dict(values=[d2['drug'],d2['price/tab'],d2['tab_count'],d2['total_price']],
               fill_color='white',
               align='left')) ])

f1.update_layout(
    height=400,
    showlegend=False,
    title_text="The Price Of " +  drug,
)            
f1.show()


