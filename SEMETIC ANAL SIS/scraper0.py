import requests
import requests
from bs4 import BeautifulSoup
import numpy as np
import json
import pandas as pd

def getdata(URL,label):
    
    strides=[]
    
    for i in range(1,50):
        
        suburl="https://www.aldiwan.net/"
    
        page = requests.get(str(URL)+str(i))
        print(i)
        links=[]
      
     
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find_all("div",class_="record col-12")
    
    
        
        for job_element in results:
        
            link=job_element.find(href=True)
            links.append(suburl+link['href'])
        
        
        for sub in links:
            
        
            page = requests.get(sub)
            soup = BeautifulSoup(page.content, "html.parser")
            results = soup.find(id="poem_content")
            results=soup.find_all('h3')
            for job_element in results:
                strides.append([(str(job_element.text).strip()),str(label)])    
    return strides


positives=getdata("https://www.aldiwan.net/Poems-Topics-%D8%BA%D8%B2%D9%84.html?page=",1)


negatives=getdata("https://www.aldiwan.net/Poems-Topics-%D8%B1%D8%AB%D8%A7%D8%A1.html?page=",0)

finaldata=np.concatenate((positives,negatives), axis=0)
np.random.shuffle(finaldata)

df2 = pd.DataFrame(finaldata,columns=['String', 'Label'])
print(df2.size)
df2=df2.dropna()
print(df2.size)
# np.savetxt("poemsentimentpos.txt", positives,fmt='%s',delimiter=',',encoding="utf-16")
# np.savetxt("poemsentimentneg.txt", negatives,fmt='%s',delimiter=',',encoding="utf-16")

df2.to_csv('poempandas.csv', encoding='utf-8-sig')
###load data examples

# loadeddata=[]

# with open('poemsentiment.txt', 'r',encoding='utf-16') as f:
#         for line in f.read().splitlines() :
#             loadeddata.append(line.split(','))
            
            
# print(loadeddata)