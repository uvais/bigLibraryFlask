
from flask import *
from searcher import *

lemon = Searcher()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/query', methods=['GET', 'POST'])
def query():
    if request.method == 'POST':
        q = request.form['q']
        result = lemon.query(q)
    return render_template('results.html', result=result)

@app.route('/data/<path:path>', methods=['GET', 'POST'])
def data(path):
    if request.method == 'GET':
        return send_from_directory('data', path)


if __name__ == '__main__':
    app.run()