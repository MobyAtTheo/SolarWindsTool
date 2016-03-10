#!/usr/bin/python2.7


import requests
import json
from getpass import getpass

###urllib3.disable_warnings()

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

def samplecode(npm_server,username,password):
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

def getLoginInfo(credsFile):
        f = open(credsFile, 'r')
	password = f.read()
        #debug: print "[-] pass: ", password.strip()
        f.close()
        return password.strip()

def main():
	#npm_server = raw_input("IP address of NPM Server: ")
	npm_server = "solarwinds.prod.xome.com"
	#username = raw_input("Username: ")
	#username = "PROD\yourusername"
	username = getLoginInfo('../creds/userfile')
	#password = getpass("Password: ")
	password = getLoginInfo('../creds/credsfile')

	samplecode(npm_server,username,password)



if __name__ == "__main__":
	main()
