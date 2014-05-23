#!/usr/bin/python
""" Class To Connect and Perfom tasks with NGIN via HTTP persistance"""

"""
The following are the functions in this class and their uses:



"""

import logging, re, httplib2, json, datetime, pprint, debug
import socks
from logging_config import *

class cie_prov:
  def __init__(self,server,url_prefix, username, password):
    
    logger = logging.getLogger("TIME")
   
    self.server = server
    self.url_prefix = url_prefix
    self.username = username
    self.password = password

  def get_cie_subscription(self, subnum):
    debug.p("**********************************************************")
    debug.p("FUNC: Class cie_prov: func:- get_cie_subscription *******")
    returncode = 100
    h = httplib2.Http(".cache")
    h.add_credentials(self.username, self.password)
    t0 = datetime.datetime.now() 
    debug.p ("http://" + self.server + self.url_prefix + subnum + " GET")
    resp, content = h.request("http://" + self.server + self.url_prefix + subnum, "GET")
    #debug.p(str(resp))
    #debug.p(str(content))
    logger.log ( INFO, "getting " + str(subnum) + " took " + str(datetime.datetime.now() - t0) )
    if int(resp["status"]) == 200:
      logger.log( INFO, "HTTP-200 successful request")
      returncode = json.loads(content)
    elif int(resp["status"]) == 404:
      logger.log( WARNING, "HTTP-404 object not found")
    else:
      logger.log( ERROR, resp["status"] + " unknown error")
    
    return returncode

	
  def get_logon_account(self, account):
    debug.p("FUNC: class cie_prov : get_logon_account **********")
#    h = httplib2.Http(".cache")
    h = httplib2.Http(proxy_info = httplib2.ProxyInfo(socks.PROXY_TYPE_HTTP, '10.103.3.22', 8080))
    h.add_credentials(self.username, self.password)
    object_prefix = "/accounts/system/security/users/"
    debug.p ("DEBUG: http://" + self.server + self.url_prefix + object_prefix + self.username + " GET")
    resp, content = h.request("http://" + self.server + self.url_prefix + object_prefix+ self.username, "GET")
    debug.p(str(resp))
    debug.p(str(content))
    return
	
  def get_https_logon_account(self, account):
    debug.p("FUNC: class cie_prov : get_https_logon_account **********")
 #   h = httplib2.Http(".cache")
    h = httplib2.Http(proxy_info = httplib2.ProxyInfo(socks.PROXY_TYPE_HTTP, '10.103.3.22', 8080))
    h.add_credentials(self.username, self.password)
    object_prefix = "/accounts/system/security/users/"
    debug.p ("DEBUG: https://" + self.server + self.url_prefix + object_prefix + self.username + " GET")
    resp, content = h.request("https://" + self.server + self.url_prefix + object_prefix+ self.username, "GET")
    debug.p(str(resp))
    debug.p(str(content))
    return
	
  def get_cie_logon(self):
    returncode = 100
    object_prefix = "/accounts/system/security/users/"
    h = httplib2.Http(".cache")
    h.add_credentials(self.username, self.password)
    t0 = datetime.datetime.now()
    debug.p ("DEBUG: http://" + self.server + self.url_prefix + object_prefix + self.username + " GET")
    resp, content = h.request("http://" + self.server + self.url_prefix + object_prefix+ self.username, "GET")
    debug.p(str(resp))
    debug.p(str(content))
    logger.log ( INFO, "getting " + str(self.username + object_prefix) + " tooks " + str(datetime.datetime.now() - t0) )
    if int(resp["status"]) == 200:
      logger.log( INFO, "HTTP-200 successful request")
      returncode = json.loads(content)
    elif int(resp["status"]) == 404:
      logger.log( WARNING, "HTTP-404 object not found")
    else:
      logger.log( ERROR, resp["status"] + " unknown error")

    return returncode



  def put_test_ep(self, data):
    h = httplib2.Http(".cache")
    h.add_credentials(self.username, self.password)
    resp, content = h.request("http://10.146.3.11:8182/cie-rest/provision/accounts/MarcSelfCare/subscriptions/S1890611201" , "PUT", json.dumps(data))
    return 


  def put_cie_endpoint(self,object, data):
    debug.p("FUNC: class cie_prov : put_cie_endpoint **********")
    h = httplib2.Http(".cache")
    h.add_credentials(self.username, self.password)
    object_prefix = "/subscriptions/"
    t0 = datetime.datetime.now() 
    resp, content = h.request("http://" + self.server + self.url_prefix + object_prefix + object, "PUT", json.dumps(data))
    logger.log ( INFO, "putting " + str(object) + " tooks " + str(datetime.datetime.now() - t0) )
    logger.log ( INFO1, " RESP | " + str(resp) )
    logger.log ( INFO1, " CONTENT | " + str(content) )
    returncode = 100 
    try:
      content_j = json.loads(content) 
    except:
      #logger.log ( ERROR, str(content) )
      logger.log ( ERROR, str(json.dumps(data)))
      return 1
    #if int(resp["status"]) == 200:  
    #  logger.log( INFO, "HTTP-200 update successfully")
    #  returncode = 0
    #elif int(resp["status"]) == 201:
    #  logger.log( INFO, "HTTP-201 create successfully")
    #  returncode = 0
    #elif int(resp["status"]) == 414:
    #  logger.log (WARNING, "HTTP-412 validation error" + content)
    #  returncode = 1
    #else:
    #  logger.log( ERROR, resp["status"] + " unknown error")
    #  returncode = 10
    if content_j["result"] == "CREATED":
      logger.log ( INFO, "Successfully created" )
      returncode = 0
    elif content_j["result"] == "UPDATED":
      logger.log ( INFO, "Successfully updated" )
      returncode = 0
    elif content_j["result"] == "VALIDATION_ERROR":
      logger.log ( ERROR, "VALIDATION_ERROR" + str(content) )
      returncode = 1
    else:
      logger.log ( ERROR, "unkown error" + str(resp) + " " + str(content) )

    #logger.log( DEBUG, resp)
    #logger.log( DEBUG, content)

    return returncode


	
  def get_cie_endpoints(self):
    returncode = 100
    object_prefix = "/endpoints"    
    #subnum = object_prefix + subnum
    h = httplib2.Http(".cache")
    h.add_credentials(self.username, self.password)
    t0 = datetime.datetime.now() 
    debug.p ("http://" + self.server + self.url_prefix + '/accounts/' + self.username + object_prefix + "GET")
    resp, content = h.request("http://" + self.server + self.url_prefix + '/accounts/' + self.username + object_prefix, "GET")
    debug.p(str(resp))
    debug.p(str(content))
    logger.log ( INFO, "getting " + str(self.username + object_prefix) + " tooks " + str(datetime.datetime.now() - t0) )
    if int(resp["status"]) == 200:
      logger.log( INFO, "HTTP-200 successful request")
      returncode = json.loads(content)
    elif int(resp["status"]) == 404:
      logger.log( WARNING, "HTTP-404 object not found")
    else:
      logger.log( ERROR, resp["status"] + " unknown error")
    
    return returncode

  def put_cie_object(self,object, data):
    h = httplib2.Http(".cache")
    h.add_credentials('admin', 'password')
    t0 = datetime.datetime.now() 
    resp, content = h.request("http://" + self.server + self.url_prefix + object, "PUT", json.dumps(data))
    logger.log ( INFO, "putting " + str(object) + " tooks " + str(datetime.datetime.now() - t0) )
    logger.log ( INFO1, " RESP | " + str(resp) )
    logger.log ( INFO1, " CONTENT | " + str(content) )
    returncode = 100 
    try:
      content_j = json.loads(content) 
    except:
      #logger.log ( ERROR, str(content) )
      logger.log ( ERROR, str(json.dumps(data)))
      return 1
    #if int(resp["status"]) == 200:  
    #  logger.log( INFO, "HTTP-200 update successfully")
    #  returncode = 0
    #elif int(resp["status"]) == 201:
    #  logger.log( INFO, "HTTP-201 create successfully")
    #  returncode = 0
    #elif int(resp["status"]) == 414:
    #  logger.log (WARNING, "HTTP-412 validation error" + content)
    #  returncode = 1
    #else:
    #  logger.log( ERROR, resp["status"] + " unknown error")
    #  returncode = 10
    if content_j["result"] == "CREATED":
      logger.log ( INFO, "Successfully created" )
      returncode = 0
    elif content_j["result"] == "UPDATED":
      logger.log ( INFO, "Successfully updated" )
      returncode = 0
    elif content_j["result"] == "VALIDATION_ERROR":
      logger.log ( ERROR, "VALIDATION_ERROR" + str(content) )
      returncode = 1
    else:
      logger.log ( ERROR, "unknown error" + str(resp) + " " + str(content) )

    #logger.log( DEBUG, resp)
    #logger.log( DEBUG, content)

    return returncode

  def put_cie_json_object(self,object, data):
      h = httplib2.Http(".cache")
      h.add_credentials('admin', 'password')
      t0 = datetime.datetime.now() 
      print ("http://" + self.server + self.url_prefix + object + "      PUT" +  (data))
      resp, content = h.request("http://" + self.server + self.url_prefix + object, "PUT", (data))
      logger.log ( INFO, "putting " + str(object) + " tooks " + str(datetime.datetime.now() - t0) )
      logger.log ( INFO1, " RESP | " + str(resp) )
      logger.log ( INFO1, " CONTENT | " + str(content) )
      returncode = 100 
      try:
        content_j = json.loads(content) 
      except:
        #logger.log ( ERROR, str(content) )
        logger.log ( ERROR, str(json.dumps(data)))
        return 1
      #if int(resp["status"]) == 200:  
      #  logger.log( INFO, "HTTP-200 update successfully")
      #  returncode = 0
      #elif int(resp["status"]) == 201:
      #  logger.log( INFO, "HTTP-201 create successfully")
      #  returncode = 0
      #elif int(resp["status"]) == 414:
      #  logger.log (WARNING, "HTTP-412 validation error" + content)
      #  returncode = 1
      #else:
      #  logger.log( ERROR, resp["status"] + " unknown error")
      #  returncode = 10
      if content_j["result"] == "CREATED":
        logger.log ( INFO, "Successfully created" )
        returncode = 0
      elif content_j["result"] == "UPDATED":
        logger.log ( INFO, "Successfully updated" )
        returncode = 0
      elif content_j["result"] == "VALIDATION_ERROR":
        logger.log ( ERROR, "VALIDATION_ERROR" + str(content) )
        returncode = 1
      else:
        logger.log ( ERROR, "unknown error" + str(resp) + " " + str(content) )

      #logger.log( DEBUG, resp)
      #logger.log( DEBUG, content)

      return returncode
	
  def get_cie_object(self,object):
    returncode = 100
    h = httplib2.Http(".cache")
    h.add_credentials(self.username, self.password)
    t0 = datetime.datetime.now() 
    debug.p ("http://" + self.server + self.url_prefix + object + "         GET")
    resp, content = h.request("http://" + self.server + self.url_prefix + object, "GET")
    #debug.p(str(resp))
    logger.log ( INFO, "getting " + str(object) + " tooks " + str(datetime.datetime.now() - t0) )
    if int(resp["status"]) == 200:
      logger.log( INFO, "HTTP-200 successful request")
      returncode = json.loads(content)
    elif int(resp["status"]) == 404:
      logger.log( WARNING, "HTTP-404 object not found")
    else:
      logger.log( ERROR, resp["status"] + " unknown error")

    return returncode    
     
    # cie errors 
    try:
      cie_error = json.loads(content)
      if not cie_error.has_key("result") or cie_error["result"] != "CREATED" and cie_error["result"] != "UPDATED":
        #logger.log( ERROR, cie_error["errors"][0]["error"])
        logger.log( ERROR, content)
        returncode = 99
      logger.log( DEBUG, content)
    except:
      logger.log ( ERROR, "unexpected content received from CIE2 during provisioning of " + str(object) + " received content: " + str(content) )
      logger.log ( DEBUG, " URl: http://" + str(self.server) + str(self.url_prefix) + str(object) )
      logger.log ( DEBUG, str(json.dumps(data)) )
      
    return returncode


  def get_cie_object_all(self,object):
      returncode = 100
      h = httplib2.Http(".cache")
      h.add_credentials(self.username, self.password)
      t0 = datetime.datetime.now() 
      debug.p ("http://" + self.server + self.url_prefix + object + '?items=100000' + "         GET")
      resp, content = h.request("http://" + self.server + self.url_prefix + object + '?items=100000' , "GET")
      #debug.p(str(resp))
      logger.log ( INFO, "getting " + str(object) + " tooks " + str(datetime.datetime.now() - t0) )
      if int(resp["status"]) == 200:
        logger.log( INFO, "HTTP-200 successful request")
        returncode = json.loads(content)
      elif int(resp["status"]) == 404:
        logger.log( WARNING, "HTTP-404 object not found")
      else:
        logger.log( ERROR, resp["status"] + " unknown error")

      return returncode    
       
      # cie errors 
      try:
        cie_error = json.loads(content)
        if not cie_error.has_key("result") or cie_error["result"] != "CREATED" and cie_error["result"] != "UPDATED":
          #logger.log( ERROR, cie_error["errors"][0]["error"])
          logger.log( ERROR, content)
          returncode = 99
        logger.log( DEBUG, content)
      except:
        logger.log ( ERROR, "unexpected content received from CIE2 during provisioning of " + str(object) + " received content: " + str(content) )
        logger.log ( DEBUG, " URl: http://" + str(self.server) + str(self.url_prefix) + str(object) )
        logger.log ( DEBUG, str(json.dumps(data)) )
        
      return returncode



  def del_cie_object(self,object):
    h = httplib2.Http(".cache")
    h.add_credentials('admin', 'password')
    t0 = datetime.datetime.now() 
    resp, content = h.request("http://" + self.server + self.url_prefix + object, "DELETE")
    logger.log ( INFO, "deleting " + str(object) + " tooks " + str(datetime.datetime.now() - t0) )
    returncode = 100 
    if int(resp["status"]) == 200:  
      logger.log( INFO, "HTTP-200 delete successfully")
      returncode = 0
    elif int(resp["status"]) == 404:
      logger.log( WARNING, "HTTP-404 object not found")
      returncode = 0
    elif int(resp["status"]) == 414:
      logger.log (WARNING, "HTTP-412 delete not allwoed")
      returncode = 1
    else:
      logger.log( ERROR, resp["status"] + " unknown error")
      returncode = 10
    return returncode


  def del_accounts_recursive(self,object):
    returncode = 100
    h = httplib2.Http(".cache")
    h.add_credentials('admin', 'password')
    resp, content = h.request("http://" + self.server + self.url_prefix + object + "/accounts?scope=self&q=", "GET")
    result = json.loads(content)
    for value in result['results']:
      print value['id']
