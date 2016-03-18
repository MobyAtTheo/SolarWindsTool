#!/usr/bin/python2.7

import xml.etree.ElementTree as ET
import re


actionFile="./mtputty_config_clean.xml"

tree = ET.parse(actionFile)
root = tree.getroot()


a=[]

def createListIP():
    for i in root.findall('.//ServerName'):
        """Get list of subfolder nodes IPs"""
        a.append(i.text)




def searchIP(a):
    searchRegex = re.compile('^10.|^172\.|^192\.168\.', re.IGNORECASE)

    l = filter(searchRegex.search, a)
    return sorted(l)



### Main

createListIP()
#sortedData=searchIP(a)

for dataSorted in searchIP(a):
    print dataSorted


