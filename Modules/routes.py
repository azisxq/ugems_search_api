from flask import Flask
from flask import jsonify
from flask import request
from Modules.common import utils
from Modules.methods import *
import pysolr
import os

solr_url = os.environ['SOLR_URL']
solr_core = os.environ['SOLR_CORE']


solr = pysolr.Solr(solr_url+solr_core, timeout=100)

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def root():
	return jsonify({'status': 'ok'}), 200


@app.route('/search', methods=['GET'])
def search():
	query = utils.validate(
		request.args, 'query',
		str, None
	)
	token = utils.validate(
		request.args,'token',
		str, None
	)
	if token is None:
		return jsonify({
			'status': 'token parameter is empty'
		}), 412

	tkn = get_token(token)
	if tkn is None:
		return jsonify({
			'status': 'incorrect input token'
		}), 412

	if query is None:
		results = solr.search('*')
	else:
		results = solr.search(query)
	res = []
	for result in results:
		result_dict = {}
		result_dict['title'] = result['title'][0]
		result_dict['content'] = result['content'][0]
		result_dict['read_role'] = result['read_role'][0]
		res.append(result_dict)
	return jsonify({
		'number of results': len(results),
		'results': res,
		'status' : 'ok'
	}), 200

