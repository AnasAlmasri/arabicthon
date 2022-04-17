import requests
import requests
from bs4 import BeautifulSoup
import numpy as np
import json

def getdata(URL,label):
    suburl="https://www.aldiwan.net/"

    page = requests.get(URL)
    links=[]
    strides=[]
 
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


positives=getdata("https://www.aldiwan.net/Poems-Topics-%D8%BA%D8%B2%D9%84.html",1)


negatives=getdata("https://www.aldiwan.net/Poems-Topics-%D8%B1%D8%AB%D8%A7%D8%A1.html",0)

finaldata=np.concatenate((positives,negatives), axis=0)
np.random.shuffle(finaldata)


np.savetxt("poemsentiment.txt", finaldata,fmt='%s',delimiter=',',encoding="utf-16")

###load data examples

loadeddata=[]

with open('poemsentiment.txt', 'r',encoding='utf-16') as f:
        for line in f.read().splitlines() :
            loadeddata.append(line.split(','))
            
            
print(loadeddata)