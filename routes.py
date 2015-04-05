
from flask import *
from searcher import *
import mysql.connector
from mysqlConnecter import *
import os
import pdf
from searcher import *
from werkzeug import secure_filename


connectMysql = mysqlConnect()
lemon = Searcher()
app = Flask(__name__)
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'

@app.route('/')
def home():
	sumSessionCounter()
	return render_template('index.html')

@app.route('/admin')
def adminhome():
	return render_template('adminlogin.html')

@app.route('/adminlogin', methods=['POST','GET'])
def login():
	if request.method == 'POST':
		u = request.form['uid']
		p = request.form['pwd']
		row = connectMysql.getMysqlQuerry(u);
		if row:
			dbuname = row[0];
			dbpass = row[1];
			if dbpass != p:
				return render_template('adminlogin.html', errormsg="Password mismatch")
			else:
				session['name'] = u
				return render_template('adminhome.html')
		else:
			return render_template('adminlogin.html', errormsg="User not found")
	elif request.method == "GET":
		if session['name']:
			return render_template('adminhome.html')
		else:
			return render_template('adminlogin.html')

@app.route('/redirect')	
def rediretHome():
	return render_template('adminhome.html')

@app.route('/logout')	
def logout():
	session.clear()
	session['name'] = None 
	return render_template('adminlogin.html')

@app.route('/query', methods=['GET', 'POST'])
def query():
    if request.method == 'POST':
        q = request.form['searchbar']
        result = lemon.query(q)
	return render_template('result.html', result=result)

def allowed_file(filename):
	ALLOWED_EXTENSIONS = set(['pdf'])
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/admin/upload', methods=['GET', 'POST'])
def upload():
	UPLOAD_FOLDER = 'pdfs'
	app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
	if request.method == 'POST':
		file = request.files.getlist('file[]')

		for uf in file:
			pdf.convert_one(uf.filename, "/home/biglibrary/bigLibraryFlask/pdfs/", "/home/biglibrary/bigLibraryFlask/files/")
		os.system("hdfs dfs -copyFromLocal /home/biglibrary/bigLibraryFlask/files/* /user/biglibrary/files")

	return render_template("adminhome.html", message="Successfully Uploaded to HDFS")

@app.route('/admin/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        os.system("hadoop jar /home/biglibrary/bigLibraryFlask/TextIndexer/target/textIndexer-1.0.jar /user/biglibrary/files")
        return render_template("adminhome.html", message="Successfully loaded to MongoDb")

@app.route('/pdfs/<path:path>', methods=['GET', 'POST'])
def data(path):
    if request.method == 'GET':
        return send_from_directory('pdfs', path)

if __name__ == '__main__':
    app.debug = True
    app.run()
