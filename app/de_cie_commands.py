import json
import os
from collections import defaultdict
from pprint import pprint


def list_subs():
	json_data = open ('./templates/subs.json')
	data = json.load (json_data)
	#print type(data)
	json_data.close()
	return data


def get_sub_details(subNo):
	json_data = open('./templates/1800131219.json')
	data = json.load (json_data)
	json_data.close()
	return data

def get_basic_translation(subNo):
	subscription = get_sub_details('1800131219')
	for index, element in enumerate(subscription['attributes']):
		if element['id'] =='basTransEpRef':
			return (subNo, element['value'])
"""
def parse_subs_list_make_sub_info(subs_list):
	# The function creates a dictionary of lists.
	newdict = defaultdict(list)
	newlist = []
	for row in subs_list:
		if row['id']:
			x = row['id'] # PICK UP FROM HERE , GET REST OF INFO FROM OTHER JSON AND ADD TO DICT.
			newdict[x].append(('id', x))
			newdict[x].append (('val', x ))
			newlist.append(newdict)
			pprint (newdict)

	return newlist
"""

def parse_subs_list_make_sub_info(subs_list):
	"""This function creates a list of dictionaries """
	
	newlist = []
	for row in subs_list:
		if row['id']:
			x = row['id']
			newdict = defaultdict(dict) 
			subNo,endpoint = get_basic_translation(x)
			newdict['id'] = x
			newdict['href'] = row['href']
			newdict['parent'] = row['parent']
			newdict['additionalInfo'] = row['additionalInfo']
			newdict['endpoint'] = endpoint
			newlist.append(newdict)
			print ""
			pprint (row)
			pprint (newdict)
			print ""
			print (newlist)

	return newlist


data_dict = list_subs()

for index, element in enumerate(data_dict["results"]):
    print element['id']
    print element['parent']
    print element['href']
    print element['uid']
    print element['additionalInfo']
    print element['additionalInfo']['accessNo']
    print type(element)

resultsOnly = data_dict['results']


print type(resultsOnly)
print resultsOnly

for subl in resultsOnly:
	print subl
	print type (subl)
	print subl['id']

vals = parse_subs_list_make_sub_info(resultsOnly)
print "VALS ----------------------"
pprint (vals)

print "***************************************"

for row in vals:
	print row['id']
	print row['additionalInfo']
	print row ['endpoint']



