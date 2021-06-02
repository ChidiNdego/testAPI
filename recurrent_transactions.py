import flask
from flask import request, jsonify
import sqlite3
import pypyodbc
import decimal
import flask.json
class MyJSONEncoder(flask.json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            # Convert decimal instances to strings.
            return str(obj)
        return super(MyJSONEncoder, self).default(obj)
app = flask.Flask(__name__)
app.json_encoder = MyJSONEncoder
app.config["DEBUG"] = True
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
@app.route('/', methods=['GET'])
def home():
    return '''<h1>Recurrent Transaction</h1>
<p>API for calling Recurrent Transactions</p>'''
@app.route('/api/v1/recurrent_txns/all', methods=['GET'])
def api_all():
   #conn = sqlite3.connect('books.db')
    conn = pypyodbc.connect('Driver={SQL Server};Server=10.234.18.152;Database=RSVREDONG;uid=edouser;pwd=Stanbic_123#')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_txns = cur.execute('SELECT * FROM Recurrent_Transactions;').fetchall()
    return jsonify(all_txns)
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404
@app.route('/api/v1/recurrent_txns', methods=['GET'])
def api_filter():
    query_parameters = request.args
    id = query_parameters.get('foracid')

    query = "SELECT * FROM Recurrent_Transactions WHERE"
    to_filter = []
    if id:
        query += ' foracid=? AND'
        to_filter.append(id)
   
    if not (id):
        return page_not_found(404)
        
    query = query[:-4] + ';'
    conn = pypyodbc.connect('Driver={SQL Server};Server=10.234.18.152;Database=RSVREDONG;uid=edouser;pwd=Stanbic_123#')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    results = cur.execute(query, to_filter).fetchall()
    return jsonify(results)
app.run()
