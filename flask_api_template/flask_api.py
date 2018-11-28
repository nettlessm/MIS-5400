# Do all the importing.
import json
import rethinkdb as r
from flask import Flask, g, render_template, abort, request

from rethinkdb.errors import RqlDriverError


# Configure the connection
RDB_HOST = 'localhost'
RDB_PORT = 28015
DB = 'News'

# Setup Flask
app = Flask(__name__)
app.config.from_object(__name__)


# Connect before a request
@app.before_request
def before_request():
    try:
        g.rdb_conn = r.connect(host=RDB_HOST, port=RDB_PORT, db=DB)
    except RqlDriverError:
        abort(503, "No database connection could be established.")

# Teardown
@app.teardown_request
def teardown_request(exception):
    try:
        g.rdb_conn.close()
    except AttributeError:
        pass

@app.route('/')
def api_help():
    return render_template('fused_news_api.html'), 200


# GET ALL /api/v1/fusednews
@app.route('/api/v1/fusednews', methods=['GET'])
def get_all_fused_news():
    fused_news = list(r.table('FusedNews').run(g.rdb_conn))
    return json.dumps(fused_news), 200


# GET ALL /api/v1/fusednews
@app.route('/api/v1/blablabla', methods=['GET'])
def get_bla():
    return 'bla'

# GET BY ID /api/v1/fusednews/<int:id>
@app.route('/api/v1/fusednews/<string:id>', methods=['GET'])
def get_fused_news_by_id(id):
    fused_news_item = r.table('FusedNews').get(id).run(g.rdb_conn)
    return json.dumps(fused_news_item)

# POST /api/v1/fusednews
@app.route('/api/v1/fusednews', methods=['POST'])
def insert_fusednews():
    fused_news_item = request.get_json()

    try:
        r.table('FusedNews').insert(fused_news_item).run(g.rdb_conn)
        return 'success', 200
    except Exception as e:
        return abort(500)

# DELETE /api/v1/fusednews/<id>
@app.route("/api/v1/fusednews/<string:id>", methods=["DELETE"])
def delete_fusednews(id):
    try:
        r.table('FusedNews').get(id).delete().run(g.rdb_conn)
        return 'success', 200
    except Exception as e:
        return abort(500)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
