import json
import os
from collections import defaultdict
from cie_connect import extract_sub_json, cie_connect
import debug


def list_subs(username, password, accountRef):
	#json_data = open ('./templates/subs.json') 
	#data = json.load (json_data)
	#json_data.close()
	debug.p( 'USER NAME is ' + str(username))
	debug.p('list_subs: PASSWORD is    : ' + str(password))
	ngin = cie_connect(username, password)
	json_obj = accountRef + '/subscriptions'
	data = ngin.get_cie_object(json_obj)

	if data['results']:
		resultsOnly = data['results']
		return resultsOnly
	else:
		return ('100')


def get_sub_details(username, password, account_name, subNo):
	subNo = str ('/' + subNo)
	json_obj = str(account_name + subNo)
	json_data = extract_sub_json (username, password, json_obj)
	#json_data = open('./templates/1800131219.json')
	data = json_data
	#data = json.load (json_data)
	#json_data.close()
	return data

def get_basic_translation(username, password, account_name, subNo):
	#subscription = get_sub_details('1800131219')
	subscription = get_sub_details(username, password, account_name , subNo)
	for index, element in enumerate(subscription['attributes']):
		if element['id'] =='basTransEpRef':
			return (subNo, element['value'])

def get_account_name():
	return '/accounts/A64560420/subscriptions'

def parse_subs_list_make_sub_info(username, password, subs_list):
	"""This function creates a list of dictionaries """
	
	newlist = []
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


def parse_subs_list(subs_list):
	pair = {}
	pairlist = []
	for sub in subs_list:
		#sub_details = get_sub_details(sub)
		subNo,endpoint = get_basic_translation(sub)
	pass 


def list_accounts (username, password, home_account):
	print username
	print password
	ngin = cie_connect(username, password)
	json_obj = (home_account + '/accounts')
	accounts_list = ngin.get_cie_object(json_obj)
	print type(accounts_list)

	return	accounts_list


def parse_accounts_list_make_account_info(username, password, accounts_list):
	"""
	This function should accept a list of accounts as input and
	should return a list of 

	"""
	def number_of_subs(ngin, ref):
		"""
		This function should accept an account reference (an account)
		and return a list of the account, the subscriptions under the account
		and the number of subscriptions in that account.
		"""
		number_of_subs = ngin.get_cie_object(ref)
		json_obj = ref + '/subscriptions'
		subscriptions = ngin.get_cie_object(json_obj)
		size = None
		subsInfo = subscriptions['results']
		size = subscriptions['totalSize']
		
		return size, subsInfo


	ngin = cie_connect(username, password)
	newlist = []
	for row in accounts_list['results']:
		if row['id']:
			totalSize, sub_info = number_of_subs(ngin, row['href']) 
			if totalSize:
				#subNo,endpoint = get_basic_translation(username, password, account_name , x)
				for line in sub_info:
					newdict = defaultdict(dict)
					debug.p("ROW    :::::::::::::::")
					debug.p(row)
					debug.p("sub_info> Line>>>::::::::::")
					debug.p(line)
					debug.p(line['id'])
					newdict['id'] = row['id']
					newdict['href'] = row['href']
					newdict['parent'] = row['parent']
					newdict['totalSize'] = totalSize
					newdict['Subscription'] = line['id']
					newdict['subHref'] = line['href']
					newlist.append(newdict)
					debug.p('NEWLIST IN LOOP::::::')
					debug.p(newlist)
				debug.p('NEWLIST ::::::::::')
				debug.p(newlist)
	return newlist








