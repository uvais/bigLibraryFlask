
from flask import *
from searcher import *
import mysql.connector
from mysqlConnecter import *


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

@app.route('/adduser', methods=['POST','GET'])
def adduser():
	if request.method == 'POST':
		username = request.form['adduseru']
		email = request.form['addusere']
		pass1 = request.form['adduserp']
		pass2 = request.form['addusercp']
		'''connectMysql.insertMysqlQuerry(username, email, pass1)
		return render_template('adminhome.html')
		'''
		res = connectMysql.insertMysqlQuerry(username, email, pass1)
		if res:
			return render_template('adminhome.html', message="Successfully added")
		else:
			return render_template('adminhome.html', message="User exists")


if __name__ == '__main__':
    app.debug = True
    app.run()
