from flask import Flask, request, jsonify, abort
from datetime import datetime
import uuid

app = Flask(__name__)

ads = {}

@app.route('/ads', methods=['POST'])
def create_ad():
    data = request.json

    required_fields = ['title', 'description', 'owner']
    if not data or not all(field in data for field in required_fields):
        abort(400, 'Missing required fields')

    ad_id = str(uuid.uuid4())

    ad = {
        'id': ad_id,
        'title': data['title'],
        'description': data['description'],
        'owner': data['owner'],
        'created_at': datetime.utcnow().isoformat()
    }

    ads[ad_id] = ad
    return jsonify(ad), 201

@app.route('/ads/<ad_id>', methods=['GET'])
def get_ad(ad_id):
    ad = ads.get(ad_id)
    if not ad:
        abort(404, 'Ad not found')
    return jsonify(ad)

@app.route('/ads/<ad_id>', methods=['PUT'])
def update_ad(ad_id):
    ad = ads.get(ad_id)
    if not ad:
        abort(404, 'Ad not found')

    data = request.json
    if not data:
        abort(400, 'Invalid JSON')

    ad['title'] = data.get('title', ad['title'])
    ad['description'] = data.get('description', ad['description'])
    ad['owner'] = data.get('owner', ad['owner'])

    return jsonify(ad)

@app.route('/ads/<ad_id>', methods=['DELETE'])
def delete_ad(ad_id):
    if ad_id not in ads:
        abort(404, 'Ad not found')

    del ads[ad_id]
    return jsonify({'status': 'deleted'}), 200

if __name__ == '__main__':
    app.run(debug=True)