#!/usr/bin/python2.7

import requests
import json
from getpass import getpass
import base64

import codecs

#Check for encoding:
#import sys  
#reload(sys)  
#sys.setdefaultencoding('utf-8')
#print "[+] default_encoding: ", sys.getdefaultencoding()

### Disable warnings
### urllib3.disable_warnings()
###/usr/lib/python2.7/dist-packages/urllib3/connectionpool.py:787: InsecureRequestWarning: Unverified HTTPS request is being made. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.org/en/latest/security.html InsecureRequestWarning)
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


"""
Make sure to set a valid nodeID in line 50 before using!

Using: http://solarwinds.prod.xome.com/Orion/NetPerfMon/NodeDetails.aspx?NetObject=N:141
BLV-SW-IDF1
"""

class SwisClient:
	def __init__(self, hostname, username, password):
		self.url = "https://%s:17778/SolarWinds/InformationService/v3/Json/" % (hostname)
		self.credentials = (username, password)

	def query(self, query, **params):
		return self._req("POST", "Query", {'query': query, 'parameters': params}).json()

	def invoke(self, entity, verb, *args):
		return self._req("POST", "Invoke/%s/%s" % (entity, verb), args).json()

	def create(self, entity, **properties):
		return self._req("POST", "Create/" + entity, properties).json()

	def read(self, uri):
		return self._req("GET", uri).json()

	def update(self, uri, **properties):
		self._req("POST", uri, properties)

	def delete(self, uri):
		self._req("DELETE", uri)

	def _req(self, method, frag, data=None):
		return requests.request(method, self.url + frag, 
			data=json.dumps(data), 
			verify=False, 
			auth=self.credentials, 
			headers={'Content-Type': 'application/json'})

def runClient(npm_server,username,password):
	swis = SwisClient(npm_server,username,password)
	
	print "Invoke Test:"
	aliases = swis.invoke("Metadata.Entity", "GetAliases", "SELECT B.Caption FROM Orion.Nodes B")
	print aliases

	print "Query Test:"
	results = swis.query("SELECT Uri FROM Orion.Nodes WHERE NodeID=@id", id=141) # set valid NodeID!
	uri = results['results'][0]['Uri']
	print uri

	print "[+] Query Test II:"
	#results = swis.query("SELECT NodeID FROM Orion.Nodes WHERE NodeID=@id", id=141) # set valid NodeID!
        results = swis.query("SELECT NodeID, ObjectSubType, IPAddress, IPAddressType, DynamicIP, Caption, NodeDescription, Description, DNS, SysName, Vendor, SysObjectID, Location, Contact, VendorIcon, Icon, IOSImage, IOSVersion, GroupStatus, StatusIcon, LastSync, LastSystemUpTimePollUtc, MachineType, Severity, ChildStatus, Allow64BitCounters, AgentPort, TotalMemory, CMTS, CustomPollerLastStatisticsPoll, CustomPollerLastStatisticsPollSuccess, SNMPVersion, PollInterval, EngineID, RediscoveryInterval, NextPoll, NextRediscovery, StatCollection, External, Community, RWCommunity, IP, IP_Address, IPAddressGUID, NodeName, BlockUntil, BufferNoMemThisHour, BufferNoMemToday, BufferSmMissThisHour, BufferSmMissToday, BufferMdMissThisHour, BufferMdMissToday, BufferBgMissThisHour, BufferBgMissToday, BufferLgMissThisHour, BufferLgMissToday, BufferHgMissThisHour, BufferHgMissToday, OrionIdPrefix, OrionIdColumn FROM Orion.Nodes WHERE NodeID=@id", id=141)
	myNodeID = results['results'][0]['IPAddress']
	print myNodeID

	print "Custom Property Update Test:"
	swis.update(uri + "/CustomProperties", city="Austin")
	swis.update(uri + "/CustomProperties", comments="O. Henry lived here")
	obj = swis.read(uri + "/CustomProperties")
	print obj

	print "Custom Property Update Test II:"
	swis.update(uri + "/CustomProperties", lastupdatedcustompropertydate="20160309") #Added a date to a custom field
	swis.update(uri + "/CustomProperties", lastupdatedcustompropertydate="")  #"delete" a custom property value
	obj = swis.read(uri + "/CustomProperties")
	print obj

	pollerUri = swis.create("Orion.Pollers", PollerType="just testing", 
		NetObject="N:" + str(obj["NodeID"]), NetObjectType="N", NetObjectID=obj["NodeID"])
	print pollerUri

	#pausePriorDelete = raw_input("Pausing prior to Delete ") #delete after test
	print "Deleting Custom Property...."
	swis.delete(pollerUri)

def getLoginInfo(credsFile,enc):
        """Get login and creds info from a file
           
           credsfile = name of file

           enc = 0 = plaintext, 1 = encoded

           use the password encode utility to create an encoded password

	   serverfile = servername or IP address
	   userfile = username (username or DOMAIN\username are acceptable)
	   credsfile = password file
        """
        password="test"
        f = codecs.open(credsFile, 'r', encoding='ascii')
	password = f.read()
        f.close()
        if enc == 0:
            return password.strip()
        else:
            decodedPW=base64.b64decode(password).encode('ascii')
            return decodedPW.strip() 
        return "busted"

def debugCredsFile(activate,npm_server,username,password):
        """Provide credsfile output information

           activate = 0 = silent (no debug output)
           activate = 1 = print to screen 

        """
        if activate == 1:
	    #npm_server = raw_input("IP address of NPM Server: ")
	    #npm_server = "solarwinds.prod.xome.com"
            print "[d] returned npm_server", npm_server,"A"
	    #username = raw_input("Username: ")
	    #username = "PROD\yourusername"
            print "[d] returned username", username
	    #password = getpass("Password: ")
            print "[d] returned password", password
        else:
            pass
            return 0

def main():
	npm_server  = getLoginInfo('../creds/serverfile',0)
	username = getLoginInfo('../creds/userfile',0)
	password = getLoginInfo('../creds/credsfile',1)

        debugCredsFile(0,npm_server,npm_server,password)

	runClient(npm_server,username,password)



if __name__ == "__main__":
	main()
