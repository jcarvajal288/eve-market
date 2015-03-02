import csv
import requests
import xml.etree.ElementTree as et

eveCentralEndpoint = "http://api.eve-central.com/api/marketstat"
jitaID = 30000142

def getItemElement(typeID):
    query = "{0}?typeid={1}&usesystem={2}".format(eveCentralEndpoint, typeID, jitaID)
    req = requests.get(query)
    xmlRoot = et.fromstring(req.text)
    return xmlRoot
    #print(req.text)


def main():
    items = []
    with open("typeids.csv", newline='') as typeidFile:
        typeids = csv.reader(typeidFile)
        for row in typeids:
            items.append(getItemElement(row[0]))
            print("added {}".format(row[1]))
    print(len(items))


if __name__ == "__main__":
    main()
    #addItem("16692", "name")
