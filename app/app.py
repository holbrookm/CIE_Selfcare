from flask import request,  Flask, render_template, url_for, redirect, flash, session
import os
from cie_connect import cie_connect, perform_cie_logon
from cie_commands import list_subs, get_sub_details, get_basic_translation, parse_subs_list_make_sub_info
from cie_commands import list_accounts, parse_accounts_list_make_account_info
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
    """
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            #return redirect(url_for('show_entries'))
            return redirect(url_for('subscriptions'))
    return render_template('mylogin.html', error=error)
    """
    if request.method == 'POST':
        debug.p ('Performing logon')
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        return_code = perform_cie_logon(session['username'], session['password']) 
        debug.p("RETURN CODE IS :")
        debug.p(return_code)
        if return_code == 100:
             error = 'Invalid password'
             flash ('The was a cock up')
             
        else:
            session['logged_in'] = True
            session['accountRef'] = return_code['accountRef']
            flash('You were logged in')
            return redirect(url_for('accounts'))
    return render_template('mylogin.html', error=error)

@app.route('/<account>/<sub_no>')
def show_sub_account(account, sub_no):
    return "You asked for sub number %s in account : " %(sub_no) 

@app.route('/accounts/<account>/subscriptions/<sub_no>')
def show_sub_details(account, sub_no):
    return "You asked for sub number %s in account : %s " %((sub_no), (account))

@app.route('/subscriptions')
def subscriptions():
    subs_list = list_subs(session['username'], session['password'],session['accountRef'])
    subscription_data_list = parse_subs_list_make_sub_info (session['username'], session['password'], subs_list)
    debug.p(type(subscription_data_list))
    return render_template('subscriptions1.html', subscription_list= subscription_data_list)
	
@app.route('/accounts')
def accounts():
    accounts_list = list_accounts(session['username'], session['password'], session['accountRef'])
    accounts_data_list = parse_accounts_list_make_account_info (session['username'], session['password'], accounts_list)
    debug.p("ACCOUNTS_LIST:::::::" + str(accounts_list))
    debug.p('ACCOUNTS_DATA_LIST :::::' + str(accounts_data_list))

    print type(accounts_data_list)
    
    return render_template('accounts.html', accounts_list= accounts_data_list)

@app.template_filter('get_id')
def get_id_filter(data):
    return data



if __name__ == "__main__":
    app.run(debug =True, port= 4500)

