
from flask import *
from searcher import *
import mysql.connector
from mysqlConnecter import *
import os
import pdf


connectMysql = mysqlConnect()
 
app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
@app.route('/')
def home():
	if request.method == 'POST':
    		if 'username' in session:
		        return 'Logged in as %s' % escape(session['username'])
		else:
			return render_template('index.html')	
	else:
	        return render_template('index.html')

@app.route('/login', methods=['POST','GET'])
def login():
	if request.method == 'POST':
		
		u = request.form['email']
		p = request.form['password']
		row = connectMysql.getMysqlQuerry(u);
		dbuname = row[0];
		dbpass = row[1];
		if dbpass != p:
			return render_template('error.html')
		else:
			session['username'] = request.form['email']
			if u == "admin":
				return render_template('adminhome.html')
			else:
				return render_template('userhome.html')


@app.route('/query', methods=['GET', 'POST'])
def query():
    if request.method == 'POST':
        q = request.form['searchbar']
        result = lemon.query(q)
	return render_template('index.html', result=result)

if __name__ == '__main__':
    app.debug = True
    app.run()
