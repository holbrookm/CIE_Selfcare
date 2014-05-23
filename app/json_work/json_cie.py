import json
import os
from pprint import pprint
import dotdictify

def list_subs():
	json_data = open ('./templates/subs.json')
	pprint (json_data)
	data = json.load (json_data)
	print type(data)
	json_data.close()
	return data


def sub_dict(somedict, somekey, default = None):
 	return dict([ (somekey, somedict.get(somekey, default)) ])


dict_out ={}
dictofsubs ={}
data_dict = list_subs()

dict_out = sub_dict(data_dict, 'results')
dictofsubs = sub_dict(dict_out, 'id')

print "%%%%%%%%%%%%%%%%%%START DOT DICTIFY %%%%%%%%%%%%%%%%%%%%%%%"
dotdict= dotdictify.dotdictify(data_dict)

print dotdict.totalSize

print dotdict.__contains__("results.id")

print "#####$$$$$ PRINT SUB DICT OF DICT_OUT & TYPE OF DICT_OUT   ^^^^^^^^^^^^^^^^"
pprint(dict_out)
print type(dict_out)

print"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"

print "New Test iteritems of sub dict DICT_OUT"
for key, value in dict_out.iteritems():
	if key == "id":
		print "EXTRACT  OF DICT INTO DICT"
		print value
	print "KEY   " + str(key)
	print "VALUE    " + str(value)



print"$$$$$$$$$$$$$$$$$-- SUB DICT , DICTOFSUBS$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"

pprint (dictofsubs)


print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!"

print "New Test DICT OF SUBS iteritems"
for key, value in dictofsubs.iteritems():
	
	print "KEY   " + str(key)
	print "VALUE    " + str(value)

print "!!!!!!!!!! DATA_DICT  - full dict !!!!!!!!!!!!!!!!!!"

pprint(data_dict)


print "!!!!!!!!!!    Single access via [][] access!!!!!!!!!!!!!!!!!!"



print "RESULTS ONLY"
print data_dict["results"]


for index, element in enumerate(data_dict["results"]):
    #print ('{} {}'.format(index, element))
    print (element)
    print element['id']
    print element['parent']
    
    print type(element)
    for k,v in enumerate(element):
    	#print ('{} {}'.format(k, v))
    	print element['id']



print "#########DICT OUT########"
dict_out = data_dict["results"]
pprint (dict_out)
print "#########################################"

print "EXTRACT ID VALUES"

print type((dict_out))



print "****************id_data"	
print data_dict.get("results")
print "******dict extract###############"


print "*********** JSON DUMPS ******************"
decode = json.dumps(data_dict)
pprint (decode)