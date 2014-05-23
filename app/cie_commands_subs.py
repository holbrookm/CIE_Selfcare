import json
import os
from collections import defaultdict
from cie_connect import extract_sub_json, cie_connect
import debug
import pprint


def list_subs(username, password, accountRef):
	""" FUNC: list_subs: 
	This functon should accept an account name and return a list of subscriptions
	from the account.
	"""
	debug.p('FUNC:::: list_subs  ::::::::::::')
	if accountRef[1] != '/':
		accountRef = '/'+ accountRef
	if accountRef[:9] != '/accounts':
		accountRef = '/accounts'+ accountRef
	
	ngin = cie_connect(username, password)
	json_obj = accountRef + '/subscriptions'
	data = ngin.get_cie_object(json_obj)
	if data == 100:
		return None
	elif data['results']:
		resultsOnly = data['results']
		return resultsOnly
	else:
		return None


def get_sub_details(username, password, account_name, subNo):
	debug.p('FUNC:::: get_sub_details  ::::::::::::')
	subNo = str ('/' + subNo)
	json_obj = str(account_name + subNo)
	json_data = extract_sub_json (username, password, json_obj)
	data = json_data
	return data

def get_basic_translation(username, password, account_name, subNo):
	#subscription = get_sub_details('1800131219')
	debug.p('FUNC:::: get_basic_translation  ::::::::::::')
	subscription = get_sub_details(username, password, account_name , subNo)
	for index, element in enumerate(subscription['attributes']):
		if element['id'] =='basTransEpRef':
			return (subNo, element['value'])
		else return None

def get_account_name():
	return '/accounts/A64560420/subscriptions'

def parse_subs_list_make_sub_info(username, password, subs_list):
	"""This function creates a list of dictionaries """
	debug.p('FUNC:::: parse_subs_list_make_sub_info  ::::::::::::')
	newlist = []
	if subs_list:
		for row in subs_list:
			if row['id']:
				account_name = get_account_name()
				newdict = defaultdict(dict)
				x = row['id'] 
				subNo,endpoint = get_basic_translation(username, password, account_name , x)
				newdict['id'] = x
				newdict['href'] = row['href']
				newdict['parent'] = row['parent']
				newdict['additionalInfo'] = row['additionalInfo']
				newdict['endpoint'] = endpoint
				newlist.append(newdict)

		return newlist
	else:
		return None


def parse_subs_list(subs_list):
	debug.p('FUNC:::: parse_subs_list  ::::::::::::')
	pair = {}
	pairlist = []
	for sub in subs_list:
		#sub_details = get_sub_details(sub)
		subNo,endpoint = get_basic_translation(sub)
	pass 


def list_accounts (username, password, home_account):
	debug.p('FUNC:::: list_accounts  ::::::::::::')
	ngin = cie_connect(username, password)
	json_obj = (home_account + '/accounts')
	accounts_list = ngin.get_cie_object(json_obj)
	return	accounts_list

def number_of_subs_10(ngin, ref):
	"""
	This function should accept an account reference (an account)
	and return a list of the account, the subscriptions under the account
	and the number of subscriptions in that account.
	"""
	debug.p('FUNC:::: number_of_subs_10  ::::::::::::')
	number_of_subs = ngin.get_cie_object(ref)
	json_obj = ref + '/subscriptions'
	subscriptions = ngin.get_cie_object(json_obj)
	size = None
	size = subscriptions['totalSize']
	subsInfo = subscriptions['results']
	next_href = subscriptions['nextPageHref']

	debug.p('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
	debug.p(next_href)
	
	return size, subsInfo, next_href

def number_of_subs_all(ngin, ref):
	"""
	This function should accept an account reference (an account)
	and return a list of the account, the subscriptions under the account
	and the number of subscriptions in that account.
	"""
	debug.p('FUNC:::: number_of_subs_all  ::::::::::::')
	number_of_subs = ngin.get_cie_object(ref)
	json_obj = ref + '/subscriptions'
	subscriptions = ngin.get_cie_object(json_obj)
	size = None
	size = subscriptions['totalSize']
	json_obj = json_obj + '?items=' +str(size) +'&scope=children'
	subscriptions = ngin.get_cie_object(json_obj)
	subsInfo = subscriptions['results']
	next_href = subscriptions['nextPageHref']

	debug.p('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
	debug.p(next_href)
	
	return size, subsInfo, next_href

def subscription_get_subType(ngin, ref):
	"""
	This function expects a connection (ngin) and account/sub ref.
	This function should accept an account/sub reference and return
	an entry for the type of Subscription.
	Choice of Advanced Service, Basic Translation, Custom Plan, SelfCare template.
	"""
	debug.p('FUNC:::: subscription_get_subType  ::::::::::::')
	data = ngin.get_cie_object(ref)
	for line in data['attributes']:
		if line['id'] == 'subType':
			subType = line['value']
			return subType



def parse_accounts_list_make_account_info(username, password, accounts_list):
	"""
	This function should accept a list of accounts as input and
	should return a list of 
	
	"""
	debug.p('FUNC:::: parse_accounts_list_make_account_info  ::::::::::::')
	ngin = cie_connect(username, password)
	newlist = []
	for row in accounts_list['results']:
		if row['id']:
			totalSize, sub_info , next_href = number_of_subs_10(ngin, row['href']) 
			if totalSize:
				for line in sub_info:
					newdict = defaultdict(dict)
					newdict['id'] = row['id']
					newdict['href'] = row['href']
					newdict['parent'] = row['parent']
					newdict['totalSize'] = totalSize
					newdict['Subscription'] = line['id']
					newdict['subHref'] = line['href']
					newdict['subType'] = subscription_get_subType(ngin, line['href'])
					newlist.append(newdict)
					#debug.p('NEWLIST IN LOOP::::::')
					#debug.p(newlist)
				#debug.p('NEWLIST ::::::::::')
				#debug.p(newlist)
	return newlist, next_href

def accounts_list_make_account_info(username, password, accounts_list):
	"""
	This function should accept a list of accounts as input and
	should return a list of parent account, account and link to subs for account
	
	"""
	debug.p('FUNC:::: accounts_list_make_account_info  ::::::::::::')
	ngin = cie_connect(username, password)
	newlist = []
	for row in accounts_list['results']:
		totalSize, sub_info , next_href = number_of_subs_10(ngin, row['href']) 
		newdict = defaultdict(dict)
		newdict['id'] = row['id']
		newdict['href'] = row['href']
		newdict['parent'] = row['parent']
		newdict['totalSize'] = totalSize
		newlist.append(newdict)
	return newlist








