import PyPDF2
import re
import requests
import json
from datetime import date


class ElasticModel:
    
    name = ""
    price = ""
    msg = ""
    date = ""
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

# pdf file object
# you can find find the pdf file with complete code in below
pdfFileObj = open('Your PDF Path', 'rb')
# pdf reader object
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
# number of pages in pdf
print(pdfReader.numPages)
# a page object
pageObj = pdfReader.getPage(0)
# extracting text from page.
# this will print the text you can also save that into String
line = pageObj.extractText() 
line = line.replace("\n","")
print(line)

matchObj = re.match( r'NAME', line, re.M|re.I)

NET_FIELDS = 4

m = [re.search('NAME : (.+?)PUBLISH', line), #Regex Name extract
     re.search('PUBLISH DATE : (.+?)PRICE', line), #Regex extract Publish Date
     re.search('PRICE : (.*)', line), #Regex extract Price
     re.search('Template 1 (.+?)ITEM', line)] #Regex extract msg

i=0
print("==> Net fields : " + str(NET_FIELDS))
eModel = ElasticModel();

while i < 4 :


    if m[i]:
    #    while matchObj is not None:        
        print("matchObj.group() : "+ m[i].group(1))

        if i == 0 : 
            eModel.name = m[i].group(1).strip()
        elif i == 1:
            eModel.date = m[i].group(1).strip()
        elif i == 2:
            eModel.price = m[i].group(1).strip()
        else:
            eModel.msg = m[i].group(1).strip()                
    else:
        print("No match!!")
    i = i+1


def __sendToElasticSearch__(elasticModel):
    print("Name : " + str(eModel))
    url = "http://localhost:9200/mypdfcollectiontest/_doc?pretty"
    data = elasticModel.toJSON()
    #data = serialize(eModel)
    response = requests.post(url, data=data,headers={
                    'Content-Type':'application/json',
                    'Accept-Language':'en'
                    
                })
    print("Url : " + url)
    print("Data : " + str(data))

    print("Request : " + str(requests))
    print("Response : " + str(response))

__sendToElasticSearch__(eModel)