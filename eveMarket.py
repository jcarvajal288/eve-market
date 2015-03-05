import argparse
import concurrent.futures
import csv
import requests
import xml.etree.ElementTree as et

eveCentralEndpoint = "http://api.eve-central.com/api/marketstat"
jitaID = 30000142
numRequests = 20

def getSystemID(systemName):
    pass

def constructItemQuery(typeID, systemName):
    systemID = getSystemID(systemName)
    query = "{0}?typeid={1}&usesystem={2}".format(eveCentralEndpoint, typeID, systemID)
    return query

def loadUrl(url):
    req = requests.get(url)
    xmlRoot = et.fromstring(req.text)
    return xmlRoot
    #print(req.text)

def launchQuery(queries, results):
    with concurrent.futures.ThreadPoolExecutor(max_workers=numRequests) as executor:
        future_to_url = {
            executor.submit(loadUrl, url): url for url in queries
        }
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            data = future.result()
            results.append(data)

def handleResults(marketResults):
    print("FINISHED: {} items polled".format(len(marketResults)))

def getSystemID(systemName):
    pass

def main(typeidFileName, system1, system2):
    marketResults = []
    with open("marketOnly_typeids.csv", newline='') as typeidFile:
        typeids = csv.reader(typeidFile)
        totalids = typeids.line_num
        urls = []
        for row in typeids:
            urls.append(constructItemQuery(row[0], system1))
            if len(urls) is numRequests:
                launchQuery(urls, marketResults)
                urls = []
                print("{}/{} items logged".format(len(marketResults), totalids))
    handleResults(marketResults)


if __name__ == "__main__":
    if sys.argc != 3:
        print("Usage: python3 eveMarket.py [TYPEID_FILE] [SYSTEM 1] [SYSTEM 2]")
    else:
        typeidFile = sys.argv[1]
        system1 = sys.argv[2]
        system2 = sys.argv[3]
        main(typeidFile, system1, system2)
