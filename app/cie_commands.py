import json
import os


def list_subs():
	json_data = open ('./templates/subs.json')
	data = json.load (json_data)
	json_data.close()
	return data
