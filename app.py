from flask import Flask, request, jsonify
from flask_cors import CORS
from elasticsearch import Elasticsearch

app = Flask(__name__)
CORS(app)

es = Elasticsearch([{'host': 'elasticsearch', 'port': 9200, 'scheme': 'http'}])

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    year = request.args.get('year', '')
    source = request.args.get('source', '')
    page = int(request.args.get('page', 1))
    size = int(request.args.get('size', 9))

    search_query = {
        "query": {
            "bool": {
                "must": [],
                "filter": []
            }
        },
        "from": (page - 1) * size,
        "size": size
    }

    if query:
        search_query["query"]["bool"]["must"].append({
            "multi_match": {
                "query": query,
                "fields": ["titulo", "subtitulo", "texto", "autor"]
            }
        })

    if year:
        search_query["query"]["bool"]["filter"].append({
            "range": {
                "data": {
                    "gte": f"{year}-01-01",
                    "lte": f"{year}-12-31"
                }
            }
        })

    if source:
        source_conditions = {
            "Rádio Cova da Beira": "rcb-radiocovadabeira.pt",
            "Rádio Caria": ["radiocaria.com", "radiocaria.pt"],
            "Rádio Clube da Covilhã": "radio-covilha.pt",
            "Notícias da Covilhã": "noticiasdacovilha.pt"
        }
        if source in source_conditions:
            condition = source_conditions[source]
            if isinstance(condition, list):
                search_query["query"]["bool"]["filter"].append({
                    "bool": {
                        "should": [{"match": {"link": c}} for c in condition],
                        "minimum_should_match": 1
                    }
                })
            else:
                search_query["query"]["bool"]["filter"].append({"match": {"link": condition}})
                
    response = es.search(index='noticias', body=search_query)
    hits = response['hits']['hits']
    return jsonify(hits)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
