import pdb
import argparse
import concurrent.futures
import csv
import requests
import xml.etree.ElementTree as et

eveCentralEndpoint = "http://api.eve-central.com/api/marketstat"
jitaID = 30000142
numRequests = 20

def getSystemID(systemName):
    with open("mapSolarSystems.csv", newline='') as systemDataFile:
        systemData = csv.reader(systemDataFile)
        for system in systemData:
            if system[3] == systemName:
                return system[2]

def constructItemQuery(typeID, systemName):
    systemID = getSystemID(systemName)
    query = "{0}?typeid={1}&usesystem={2}".format(eveCentralEndpoint, typeID, systemID)
    return query

def loadUrl(url):
    req = requests.get(url)
    xmlRoot = et.fromstring(req.text)
    return xmlRoot

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

def main(typeidFileName, system1, system2):
    marketResults = []
    with open(typeidFileName, newline='') as typeidFile:
        typeids = csv.reader(typeidFile)
        #totalids = typeids.line_num
        urls = []
        for row in typeids:
            urls.append(constructItemQuery(row[0], system1))
            if len(urls) is numRequests:
                launchQuery(urls, marketResults)
                urls = []
                print("{}/{} items logged".format(len(marketResults), totalids))
        else: # launch queries for any leftover items
            launchQuery(urls, marketResults)
    handleResults(marketResults)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('system1', type=str, help="if just system1 is supplied, will compare buy and sell orders in that system")
    parser.add_argument('system2', type=str, help="if system2 is supplied as well, will compare the sell orders in those two systems")
    parser.add_argument('--ids', type=str, help="the list of item ids to use")
    args = parser.parse_args()
    main(args.ids, args.system1, args.system2)
