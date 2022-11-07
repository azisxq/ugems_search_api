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


@app.route('/token',methods=['POST','GET'])
def token():
	if request.method == 'POST':
		try:
			create_token()
		except Exception as e:
			print(e)
			return jsonify({
				'status': "problem with creating token"
			}), 403
		try:
			tkn = get_token()
		except Exception as e:
			print(e)
			return jsonify({
				'status': "problem when get token"
			}), 403
		return jsonify({
			'token': tkn,
			'status': "ok"
		}), 200
	elif request.method == 'GET':
		try:
			tkn = get_token()
		except Exception as e:
			print(e)
			return jsonify({
				'status': "problem when get token"
			}), 403
		return jsonify({
			'token': tkn,
			'status': "ok"
		}), 200


@app.route('/search', methods=['GET'])
def search():
	query = utils.validate(
		request.args, 'query',
		str, None
	)
	try:
		token = request.headers['token']
	except :
		token = None
	if token is None:
		return jsonify({
			'status': 'token parameter is empty'
		}), 412

	tkn = search_token(token)
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
		result_dict['read_role'] = result['read_role']
		try:
			result_dict['link'] = result['link'][0]
		except:
			result_dict['link'] = 'https://ugems.id/o/headless-delivery/v1.0/blog-postings/44887/rendered-content-by-display-page/test'
		try:
			result_dict['source'] = result['source'][0]
		except:
			result_dict['source'] = 'sharepoint'
		res.append(result_dict)
	return jsonify({
		'number of results': len(results),
		'results': res,
		'status' : 'ok'
	}), 200

