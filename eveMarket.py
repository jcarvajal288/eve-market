import concurrent.futures
import csv
import pdb
import requests
import xml.etree.ElementTree as et

eveCentralEndpoint = "http://api.eve-central.com/api/marketstat"
jitaID = 30000142
numRequests = 20

def constructItemQuery(typeID):
    query = "{0}?typeid={1}&usesystem={2}".format(eveCentralEndpoint, typeID, jitaID)
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
    print("FINISHED")

def countLines(idsFile):
    return sum(1 for line in idsFile)

def main():
    marketResults = []
    pdb.set_trace()
    with open("marketOnly_typeids.csv", newline='') as typeidFile:
        typeids = csv.reader(typeidFile)
        totalids = countLines(typeidFile)
        urls = []
        for row in typeids:
            urls.append(constructItemQuery(row[0]))
            if len(urls) is numRequests:
                launchQuery(urls, marketResults)
                urls = []
                print("{}/{} results polled".format(len(marketResults), totalids))
    handleResults(marketResults)


if __name__ == "__main__":
    main()
