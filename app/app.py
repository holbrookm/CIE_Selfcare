import sys
sys.path.append('/Users/holbrookm/Virtualenvs/CIE_Selfcare/app/basicSubscription')

from flask import request,  Flask, render_template, url_for, redirect, flash, session
import os
from cie_connect import cie_connect, perform_cie_logon
from cie_commands import list_subs, get_sub_details, get_basic_translation
from cie_commands import parse_subs_list_make_sub_info
from cie_commands import list_accounts, accounts_list_make_account_info
from cie_commands import get_endpoint_info
from cie_commands_endpoints import list_endpoints, modify_list_endpoints_all
from cie_commands_basicsub import setSub, changeBasicEndpoint
import debug


#create the application
app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='developmentkey',
    #USERNAME='holbrookm',
    #PASSWORD='manu16'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.route('/')
def index():
	return render_template('mylogin.html')



"""
@app.route('/add', methods= ['POST',])
def add_todo():
	if 'todo_item' in request.form:
		todo =TodoItem(description = request.form['todo_item'])
		db.session.add(todo)
		db.session.commit()
		return redirect(url_for ('.index'))
	return "Error!"
"""


@app.route('/login', methods=['POST', ])
def login():
    error = None
    if request.method == 'POST':
        debug.p ('Performing logon')
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        return_code = perform_cie_logon(session['username'], session['password']) 
        if return_code == 100:
             error = 'Invalid password'
             flash(u'Invalid password provided', 'error')
             
        else:
            session['logged_in'] = True
            session['accountRef'] = return_code['accountRef']
            return redirect(url_for('accounts'))
    return render_template('mylogin.html', error=error)

@app.route('/<account>/<sub_no>')
def show_sub_account(account, sub_no):
    debug.p('FUNC:::::: app.route.show_sub_account')
    return "You asked for sub number %s in account : " %(sub_no) 

@app.route('/accounts/<account>/subscriptions/<sub_no>')
def show_sub_details(account, sub_no):
    debug.p('FUNC:::::: app.route.show_sub_details')    
    return "You asked for sub number %s in account : %s " %((sub_no), (account))


@app.route('/accounts/<account>/subscriptions/<sub_no>/modify', methods=['POST', 'GET',])
def modify_basic_sub(account, sub_no):
    debug.p('FUNC:::::: app.route.subscriptions.modify_basic_sub')
    if request.method == 'POST':
        return "You asked for sub number %s in account : %s " %((value), (value))
    else:
        href = request.path
        href = href[0:-7]
        print ('HREF ++ ') + str(href) 
        #return "You asked for sub number %s in account : %s " %((sub_no), (account))
        termNo = get_basic_translation(session['username'], session['password'], href)
        endpoints_list = modify_list_endpoints_all(session['username'], session['password'], session['accountRef'])
        
        if endpoints_list == None or termNo == None:
            return (' ERROR ERROR ERROR')
        else:
            return render_template('modifyBasic.html', subscription = sub_no, termNumber = termNo,endpoints = endpoints_list ,basehref = session['accountRef'])


@app.route('/accounts/<account>/subscriptions/<sub_no>/applyBasic', methods=['POST',])
def applyBasic(account, sub_no):
    debug.p('FUNC:::::: app.route.applyBasic')
    if request.method == 'POST':
        endpoint = request.form['modsub']
        account = '/accounts/' + account + "/subscriptions"
        if (changeBasicEndpoint(session['username'], session['password'], account, sub_no, endpoint)):
            #return render_template('accounts.html')
            message =  ("The Endpoint for subscription " + sub_no + "has been changed to : " + endpoint)
            flash(message, 'success')
            return redirect(url_for('accounts'))
        else:
            return ('ERROR ')
        #return "You asked for sub number %s in account : %s " %((endpoint), (endpoint))
    else:
            return (' ERROR ERROR ERROR')
        
@app.route('/accounts/<account>/subscriptions')
def subscriptions(account):
    #The following command can be used for landing pages and it takes a session AccountRef from NGIN
    # for the account ref landing
    #subs_list = list_subs(session['username'], session['password'],session['accountRef'])
    debug.p('FUNC:::::: app.route.subscriptions')
    subs_list = list_subs(session['username'], session['password'],account)
    subscription_data_list = parse_subs_list_make_sub_info (session['username'], session['password'], subs_list)
    debug.p(subscription_data_list)
    if subscription_data_list == None:
        return (' ERROR ERROR ERROR')
    else:
        return render_template('subscriptions1.html', subscription_list= subscription_data_list, basehref = session['accountRef'])


@app.route('/accounts/<account>/endpoints/<endpoint>')
def endpoint(account, endpoint):
    #The following command can be used for landing pages and it takes a session AccountRef from NGIN
    # for the account ref landing
    #subs_list = list_subs(session['username'], session['password'],session['accountRef'])
    debug.p('FUNC:::::: app.route.endpoint')
    endpoint_info = get_endpoint_info(session['username'], session['password'], request.path)
    if endpoint_info == None:
        return (' ERROR ERROR ERROR')
    else:
        return render_template('endpoint.html', endpoint = endpoint_info, basehref = session['accountRef'])

@app.route('/accounts')
def accounts():
    # accounts list will be a list of accounts under the HOME account
    # it contains parent, id, uid and href of the accounts
    debug.p('FUNC:::::: app.route.accounts')
    debug.p(session['accountRef'])
    flash(u'You were logged in', 'success')
    accounts_list = list_accounts(session['username'], session['password'], session['accountRef'])
    # accounts_data_list will be a list of parent account, account and link to subs for accounts in accounts_list
    # it contains id, href and parent.
    accounts_data_list = accounts_list_make_account_info (session['username'], session['password'], accounts_list)
    
    return render_template('accounts.html', accounts_data_list= accounts_data_list, basehref = session['accountRef'])

@app.route('/accounts/<account>/endpoints')
def endpoints_list(account):
    #The following command can be used for landing pages and it takes a session AccountRef from NGIN
    # for the account ref landing
    #subs_list = list_subs(session['username'], session['password'],session['accountRef'])
    debug.p('FUNC:::::: app.route.endpoints_list')
    endpoints_list, nextPage, lastPage, numberOfEndpoints = list_endpoints(session['username'], session['password'], session['accountRef'])
    if endpoints_list == None:
        return (' ERROR ERROR ERROR')
    else:
        return render_template('endpoints.html', endpoints = endpoints_list, nextPage= nextPage, lastPage=lastPage, basehref = session['accountRef'])


# Below this point the filters are stored    

@app.template_filter('rsplit')
def get_id_filter(data):
    if data:
        return data.rsplit('/')[-1]
    else:
        return



if __name__ == "__main__":
    app.run(debug =True, port= 4500)

