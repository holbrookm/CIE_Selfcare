import json
import os
import pprint as pprint
import class_cie_con_mod
from collections import defaultdict
from cie_connect import extract_sub_json, cie_connect
import debug
from classBasicSubscription import BasicSubscription, Attributes, jdefault

def setSub(id_property = None, last_modified = None, created = None, allow_tags = None, attributes = None):
	""" This subscription should use the class classBasicSubscription to create the json
	for the modify basic subscription command.
	"""
	debug.p("FUNC::::: cie_commands_basicsub.setSub()::::   input is subscription number")


	sub = BasicSubscription()
	sub.id = id_property
	sub.lastModified = last_modified
	sub.created = created
	sub.allowTags = allow_tags
	sub.attributes = [attributes]

	debug.p('#####################################################')
	json_string = (json.dumps(sub, default = jdefault))
	return json_string


def get_sub_details(username, password, account_name, subNo):
	debug.p('FUNC:::: get_sub_details  ::::::::::::')
	subNo = str ('/' + subNo)
	json_obj = str(account_name + subNo)
	data = extract_sub_json (username, password, json_obj)
	return data, json_obj


def changeBasicEndpoint(username, password, account_name, subNo, endpoint):
	ngin = cie_connect(username,password)

	debug.p('FUNC:::: get_changeNasicEndpoint  ::::::::::::')

	attrib = Attributes()
	attrib.id = "basTransEpRef"
	attrib.value = endpoint

	subData, href = get_sub_details(username, password, account_name, subNo)
	lastModified = subData['lastModified']
	attributes = attrib
	created = subData['created']
	allowTags = subData['allowTags']
	id_property = subData['id']

	json_string = setSub(id_property, lastModified, created, allowTags, attributes)

	exitCode = ngin.put_cie_json_object(href, json_string)
	if exitCode == 0:
		return True
	else:
		return None
