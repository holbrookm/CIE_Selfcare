import json
import os
from collections import defaultdict
from cie_connect import cie_connect
import debug
import pprint


def list_endpoints(username, password, accountRef):
	#json_data = open ('./templates/subs.json') 
	#data = json.load (json_data)
	#json_data.close()
	""" FUNC: list_subs: 
	This functon should accept an account name and return a list of endpoints
	from the account. Example of data returned.

	parent" : "/accounts/AGerry",
    "id" : "0019724025059",
    "uid" : null,
    "href" : "/accounts/AGerry/endpoints/0019724025059",
    "additionalInfo" : {
    }

	"""
	debug.p('FUNC:::: list_endpoints  ::::::::::::' + 'Input Parameter is : ' + str(accountRef))
	if accountRef[0] != '/':
		accountRef = '/'+ accountRef
	if accountRef[:9] != '/accounts':
		accountRef = '/accounts'+ accountRef
	
	ngin = cie_connect(username, password)
	json_obj = accountRef + '/endpoints'
	data = ngin.get_cie_object(json_obj)

	debug.p(data)
	if data == 100:
		return None
	elif data['results']:
		resultsOnly = data['results']
		nextPageHref = data['nextPageHref']
		lastPageHref = data['lastPageHref']
		numberOfEndpoints = data['totalSize']
		return resultsOnly , nextPageHref, lastPageHref, numberOfEndpoints
	else:
		return None


def modify_list_endpoints_all(username, password, accountRef):
	#json_data = open ('./templates/subs.json') 
	#data = json.load (json_data)
	#json_data.close()
	""" FUNC: list_subs: 
	This functon should accept an account name and return a list of endpoints
	from the account. Example of data returned.

	parent" : "/accounts/AGerry",
    "id" : "0019724025059",
    "uid" : null,
    "href" : "/accounts/AGerry/endpoints/0019724025059",
    "additionalInfo" : {
    }

	"""
	debug.p('FUNC:::: list_endpoints  ::::::::::::' + 'Input Parameter is : ' + str(accountRef))
	if accountRef[0] != '/':
		accountRef = '/'+ accountRef
	if accountRef[:9] != '/accounts':
		accountRef = '/accounts'+ accountRef
	
	ngin = cie_connect(username, password)
	json_obj = accountRef + '/endpoints'
	data = ngin.get_cie_object_all(json_obj)

	debug.p(data)
	if data == 100:
		return None
	elif data['results']:
		resultsOnly = data['results']
		return resultsOnly
	else:
		return None


def get_endpoint_info(username, password, endpoint):
	"""
	This function should accept an endpoint and return the json.
	"""
	debug.p('FUNC:::: get_endpoint_info  ::::::::::::')
	ngin = cie_connect(username, password)
	data = ngin.get_cie_object(endpoint)
	return data





