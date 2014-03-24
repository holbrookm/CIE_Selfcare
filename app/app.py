from flask import request,  Flask, render_template, url_for, redirect, flash, session
import os
from cie_connect import cie_connect
from cie_commands import list_subs



#create the application
app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='mholbrook@eircom.net',
    PASSWORD='manu16'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.route('/')
def index():
	return render_template('mylogin.html')


@app.route('/account', methods =['POST',])
def account():
	if "username" in request.form:
		print request.form['password']
		return request.form['password']
	return render_template("hello.html")
	#print request.form


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
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            #return redirect(url_for('show_entries'))
            return redirect(url_for('dummy'))
    return render_template('mylogin.html', error=error)

@app.route('/dummy')
def dummy():
	acs_list = list_subs()
	return render_template('dummy.html', var_list= acs_list)
	


if __name__ == "__main__":
    app.run(debug =True, port= 4500)

