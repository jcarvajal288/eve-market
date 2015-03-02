import csv
import requests
import xml.etree.ElementTree as et

eveCentralEndpoint = "http://api.eve-central.com/api/marketstat"
jitaID = 30000142

def addItem(typeID, name):
    query = "{0}?typeid={1}&usesystem={2}".format(eveCentralEndpoint, typeID, jitaID)
    req = requests.get(query)
    xmlRoot = et.fromstring(req.text)
    print(xmlRoot.tag)


def main():
    products = []
    with open("typeids.csv", newline='') as typeidFile:
        typeids = csv.reader(typeidFile)
        for row in typeids:
            products.append(addItem(row[2], row[1]))


if __name__ == "__main__":
    #main()
    addItem("16692", "name")
