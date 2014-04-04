import class_cie_con_mod

testplant1=  '172.30.1.1'

def cie_connect(username, password):
    prov = class_cie_con_mod.cie_prov( str(testplant1 + ':8182'), "/cie-rest/provision", username, password)
    return prov


def extract_sub_json (username, password, sub):
    """ To extract subscription json. """
    ngin = cie_connect (username, password)
    sub_data = ngin.get_cie_subscription(sub)
    return sub_data

def perform_cie_logon (username, password):
	ngin = cie_connect (username, password)
	return_code = ngin.get_cie_logon()
	return return_code