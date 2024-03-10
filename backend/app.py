import redis
import pickle

from flask import Flask, jsonify, request
from alembic.config import Config
from alembic import command

redis_conn = redis.StrictRedis('redis')
alembic_cfg = Config("./db/alembic.ini")

app = Flask(__name__)


@app.route('/revision', methods=['POST'])
def generate_revision():
    body = request.get_json()
    entries = body["entries"]
    
    entries = pickle.dumps(entries)
    redis_conn.set('migration_entries', entries)
    command.revision(alembic_cfg, autogenerate=True, message="update")
    
    return jsonify('ok'), 200

@app.route('/upgrade', methods=['POST'])
def upgrade_dwh():
    command.upgrade(alembic_cfg, "head")
    
    return jsonify('ok'), 200

@app.route('/downgrade', methods=['POST'])
def downgrade_dwh():
    command.downgrade(alembic_cfg, "-1")
    
    return jsonify('ok'), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)