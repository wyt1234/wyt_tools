import numpy as np
import spacy

from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import logging

from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)
api = Api(app)

app.logger.info('LOADING SPACY MODEL')
# python3 -m spacy download  zh_core_web_lg
nlp = spacy.load('zh_core_web_lg')

app.logger.info('READY APP')

parser_answer = reqparse.RequestParser()
parser_answer.add_argument('sentences')


def sentences_similarity(sentences, mode='spacy'):
    similarities = []

    if mode == 'spacy':
        for n, s in enumerate(sentences):
            for q in sentences[n + 1:]:
                token_s = nlp(s)
                token_q = nlp(q)
                simil = token_s.similarity(token_q)
                app.logger.info('simil {}'.format(float(simil)))
                similarities.append(float(simil))

    return {'error': False, 'similarity': similarities}


# 返回vector
def sentences_embedding(sentences):
    embeddings = []

    for n, s in enumerate(sentences):
        token_s = nlp(s)
        # app.logger.info('vector {}'.format(float(token_s)))
        embeddings.append(token_s.vector.tolist())
    return {'error': False, 'embeddings': embeddings}


class SimilaritySP(Resource):
    def get(self):
        return {"error": True, "message": 'not_implemented'}

    def post(self):

        app.logger.info('SIMILARITY {}'.format('POST CALLED'))

        json_sentences = request.get_json(force=True)

        try:
            sentences = json_sentences['sentences']

            if len(sentences) < 1 and isinstance(sentences, list):
                return {'error': True, 'message': 'NOT_ENOUGH_SENTENCES'}
            error = sentences_similarity(sentences, mode='spacy')

            if error['error'] == False:

                return {'error': False, 'similarity': error['similarity']}
            else:
                return error

        except Exception as e:
            app.logger.info('SIMILARITY ERROR {} {}'.format('POST PARSER', e))
            return {'error': True, 'message': 'ERROR_PARSER'}


# 新增：只返回spacy的embedding
class TokenSP(Resource):
    def get(self):
        return {"error": True, "message": 'not_implemented'}

    def post(self):
        app.logger.info('SIMILARITY {}'.format('POST CALLED'))
        json_sentences = request.get_json(force=True)
        sentences = json_sentences['sentences']
        if len(sentences) == 0 and isinstance(sentences, list):
            return {'error': True, 'message': 'NOT_ENOUGH_SENTENCES'}
        error = sentences_embedding(sentences)
        if error['error'] == False:
            return {'error': False, 'embedding': error['embeddings']}
        else:
            return error


'''
curl -d '{"sentences": ["hello world", "hello world"]}' -H 'Content-Type: application/json' -X POST localhost:8000/get_similarity/

curl --location --request POST 'localhost:8082/get_sp_embeddings/' \
--header 'Content-Type: application/json' \
--data-raw '{"sentences": ["你好你好你好2"]}'

'''
api.add_resource(SimilaritySP, '/get_similarity_sp/')
api.add_resource(TokenSP, '/get_sp_embeddings/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082, debug=True)
