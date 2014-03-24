import json
import os
from pprint import pprint

def list_subs():
	json_data = open ('./templates/subs.json')
	data = json.load (json_data)
	print data
	json_data.close()
	return data


data_dict = list_subs()

pprint(data_dict)

print data_dict["results"][2]["id"]